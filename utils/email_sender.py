import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import EMAIL_ADDRESS, EMAIL_PASS, EMAIL_NAME
from loguru import logger
import ssl
from email.utils import formatdate

def send_verification_email(nameofuser: str, receiver: str, token: str):
    logger.info(
        f"Sending mail to address {receiver} with token {token} name of user are {nameofuser}"
    )
    context = ssl.create_default_context()
    smtp_server = "smtp.seznam.cz"
    port = 465  # For starttls
    sender_email = EMAIL_NAME
    password = EMAIL_PASS
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Tvůj ověřovací kód pro Discord server VetUni"
        msg["From"] = "Aina BOT <aina@jevlk.cz>"
        msg["To"] = receiver
        msg["Date"] = formatdate()

        # Create the body of the message (a plain-text and an HTML version).
        text = "Ahoj {0}, tvůj ověřovací kód je: {1}".format(
            nameofuser, token
        )
        html = """
        <html>
        <head></head>
        <body>
            <p>Ahoj {0},<br>
            tvůj ověřovací kód je: <b>{1}</b><br>
            Vlož ho do políčka, které se ti zobrazilo na Discordu.
            Pokud nevíš, o co se jedná, tak můžeš tento email směle ignovat :D
        </body>
        </html>
        """.format(
            nameofuser, token
        )

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        server.sendmail(sender_email, receiver, msg.as_string())

def send_registration_email(user):
    sender = "aina@jevlk.cz"
    receiver = "aina@jevlk.cz"
    message = f"New user registered: {user.name} ({user.id})"
    msg = MIMEText(message)
    msg["Subject"] = "New User Registration"
    msg["From"] = sender
    msg["To"] = receiver

    context = ssl.create_default_context()
    smtp_server = "smtp.seznam.cz"
    port = 465  # For starttls
    sender_email = EMAIL_NAME
    password = EMAIL_PASS

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver, msg.as_string())
