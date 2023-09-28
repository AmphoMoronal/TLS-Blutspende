# Default Python libraries
import random
import string
import requests
import os

# database & env
from db import session, Doners
from dotenv import load_dotenv

# Mail imports
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


load_dotenv()


def new_uid():
    user_id = ""
    for i in range(4):
        user_id += ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        if i != 3:
            user_id += "-"

    while True:
        doner_id = session.query(Doners).filter(Doners.user_id == user_id).first()
        if not doner_id:
            break

    return user_id


def check_doner(mail):
    doner = session.query(Doners).filter(Doners.email == mail).first()
    if doner:
        return doner.user_id

    if not doner:
        return None


def reset_doners():
    doners = session.query(Doners).all()
    for doner in doners:
        doner.appointment = False


def get_iserv_provider_cfg():
    return requests.get(os.getenv("ISERV_DISCORVERY_URL")).json()


def send_confirmation_email(current_user, date, time):
    subject = "Erfolgreiche Buchung Ihres Blutspendentermines"
    body = (f"Guten Tag {current_user.name},\nDies ist ihre Buchungsbestätigung.\n\n"
            f"Ihr termin findet am {date.replace('-', '.', 2)} um {time[:2]}:{time[2:]} statt. \n"
            f"Bitte kommen Sie in Raum 40 in der Theodor-Litt Schule in Gießen\n"
            f"\nMit freundlichen Grüßen\n"
            f"Ihr Blutspendeteam der Theodor-Litt Schule Gießen in Kooperation des UKGM Gießen - Marburg\n"
            f"Mail: blutspenden@tls-giessen.eu\n"
            f"Tel: 0641/123456789")
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = current_user.email
    password = os.getenv("EMAIL_PASSWORD")

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = "test.pdf"  # In same directory as script

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP(os.getenv("SMTP_SERVER"), os.getenv("STARTTLS_PORT")) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
