import smtplib
import ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

subject = "Erfolgreiche Buchung des Blutspendentermines"
body = "Guten Tag Luis Herr,\nDies ist ihre Buchungsbestätigung."
sender_email = os.getenv("SENDER_EMAIL")
receiver_email = "luis.herr@tls-giessen.eu"
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
# message.attach(part)
text = message.as_string()

# Log in to server using secure context and send email
context = ssl.create_default_context()
with smtplib.SMTP(os.getenv("SMTP_SERVER"), os.getenv("STARTTLS_PORT")) as server:
    server.starttls(context=context)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)

