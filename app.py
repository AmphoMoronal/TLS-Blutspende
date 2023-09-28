# Python standard libraries
import os
import json
import requests

# Third-party libraries
from flask import Flask, redirect, request, url_for, render_template
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
from dotenv import load_dotenv

import utils
# Internal imports
from doner import Doner
from appointment import Appointment
from utils import new_uid, check_doner, get_iserv_provider_cfg

load_dotenv()

# Configuration
ISERV_CLIENT_ID = os.getenv("ISERV_CLIENT_ID")
ISERV_CLIENT_SECRET = os.getenv("ISERV_CLIENT_SECRET")
ISERV_DISCOVERY_URL = os.getenv("ISERV_DISCORVERY_URL")
TEMPLATES_AUTO_RELOAD = True

# Flask app setup
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") or os.urandom(24)

# User session management setup
login_manager = LoginManager()
login_manager.init_app(app)

# OAuth client setup
client = WebApplicationClient(ISERV_CLIENT_ID)


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return Doner.get(user_id)


# Index route which is the first route the users see
@app.route("/")
def index():
    # user logged in
    if current_user.is_authenticated:
        return redirect(url_for("questions"))

    # user not logged in
    else:
        return render_template("login.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    users_name = request.form["name"]
    users_email = request.form["email"]
    unique_id = check_doner(users_email)
    if not unique_id:
        unique_id = new_uid()

    # Create a user in your db with the information provided
    user = Doner(
        id_=unique_id, name=users_name, email=users_email
    )

    # Add User to the database
    if not Doner.get(unique_id):
        Doner.create(unique_id, users_name, users_email)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))


@app.route("/iservlogin")
def iservlogin():
    # Find out what URL to hit for iserv login
    iserv_provider_cfg = get_iserv_provider_cfg()
    authorization_endpoint = iserv_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for iserv login and provide scopes that let you
    # retrieve user's profile from iserv
    return redirect(client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    ))


@app.route("/iservlogin/callback")
def callback():
    # Get authorization code iserv sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for things on behalf of a user
    iserv_provider_cfg = get_iserv_provider_cfg()
    token_endpoint = iserv_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(ISERV_CLIENT_ID, ISERV_CLIENT_SECRET),
    )

    # Parse the tokens
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = iserv_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    unique_id = userinfo_response.json()["sub"]
    users_email = userinfo_response.json()["email"]
    users_name = userinfo_response.json()["name"]

    # Create a user in your db with the information provided
    user = Doner(
        id_=unique_id, name=users_name, email=users_email
    )

    # User doesn't exist? Add it to the database.
    if not Doner.get(unique_id):
        Doner.create(unique_id, users_name, users_email)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/questions")
def questions():
    if current_user.is_authenticated:
        return render_template("questions.html")

    else:
        return redirect(url_for("index"))


@app.route("/checkdonator", methods=['GET', 'POST'])
def checkdonator():
    if current_user.is_authenticated:
        adult: bool = bool(request.form.get('adult'))
        weight: bool = bool(request.form.get('weight'))
        healthy: bool = bool(request.form.get('healthy'))
        tattoos: bool = not bool(request.form.get('tattoos'))

        # checks if the blood is donatable
        values = [adult, weight, healthy, tattoos]
        not_donatable = []

        for value in values:
            if not value:
                not_donatable.append(value)

            else:
                pass

        if not_donatable:
            return render_template("not_donatable.html")

        else:
            return redirect(url_for("appointments"))

    else:
        return redirect(url_for("index"))


@app.route("/appointments")
def appointments():
    if current_user.is_authenticated:
        # REMOVE WHEN ADMIN PANEL IS ACTIVE
        Appointment.add_appointment("18-09-2023")
        return render_template("appointments.html",
                               appointments=Appointment.get_appointment("18-09-2023"),
                               free_slots=Appointment.free_slots)

    else:
        return redirect(url_for("index"))


@app.route("/set_appointment", methods=["GET", "POST"])
def set_appointment():
    if current_user.is_authenticated:
        time = request.args.get('time'),
        date = Appointment.get_date()[0]
        Appointment.add_doner(date, time[0], current_user.user_id)
        utils.send_confirmation_email(current_user, date, time[0])
        return render_template("confirmation.html", time_slot=time[0], date=date,
                               current_user=current_user)

    else:
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(ssl_context="adhoc", port=5000, use_reloader=True)
