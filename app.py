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


# Internal imports
from user import User
from utils import new_uid, check_spender

load_dotenv()

# Configuration
ISERV_CLIENT_ID = os.getenv("ISERV_CLIENT_ID")
ISERV_CLIENT_SECRET = os.getenv("ISERV_CLIENT_SECRET")
ISERV_DISCOVERY_URL = os.getenv("ISERV_DISCORVERY_URL")

# Flask app setup
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") or os.urandom(24)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# Naive database setup
# init_db_command()


# OAuth 2 client setup
client = WebApplicationClient(ISERV_CLIENT_ID)


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def index():
    return render_template("login.html")
    # if current_user.is_authenticated:
    #     return (
    #         "<p>Hello, {}! You're logged in!\nEmail: {}</p>"
    #         '<a class="button" href="/logout">Logout</a>'.format(
    #             current_user.name, current_user.email
    #         )
    #     )
    # else:
    #     return ('<a class="button" href="/loginiserv">IServ Login</a>'
    #             '<div data-role="fieldcontain" >'
    #             '<fieldset >'
    #             '<label for="name"> Voller Name </label>'
    #             '<input type="text" name="name" id="name" focus >'
    #             '<label for="email"> E-Mail </label>'
    #             '<input type="text" name="email" id="email">'
    #             '<a class="button" href="/login">Weiter</a>>'
    #             '</fieldset >'
    #             '</div >')


@app.route("/loginiserv")
def loginiserv():
    # Find out what URL to hit for iserv login
    iserv_provider_cfg = get_iserv_provider_cfg()
    authorization_endpoint = iserv_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for iserv login and provide
    # scopes that let you retrieve user's profile from iserv
    return redirect(client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    ))


@app.route('/login', methods=['GET', 'POST'])
def login():
    users_name = request.form["name"]
    users_email = request.form["email"]
    unique_id = check_spender(users_email)
    if not unique_id:
        unique_id = new_uid()

    # Create a user in your db with the information provided
    user = User(
        id_=unique_id, name=users_name, email=users_email
    )

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))


@app.route("/loginiserv/callback")
def callback():
    # Get authorization code iserv sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
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
    user = User(
        id_=unique_id, name=users_name, email=users_email
    )

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    print("called")
    logout_user()
    print("logged out")
    return redirect(url_for("index"))


def get_iserv_provider_cfg():
    return requests.get(ISERV_DISCOVERY_URL).json()


if __name__ == "__main__":
    app.run(ssl_context="adhoc")
