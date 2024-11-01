import re
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from schemas import ClientSchema


def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


async def send_message(sender: ClientSchema, recipient: ClientSchema, message: str):
    conf = ConnectionConfig(
        MAIL_USERNAME=sender.email,
        MAIL_PASSWORD=sender.password,
        MAIL_FROM=sender.email,
        MAIL_FROM_NAME="{} {}".format(sender.first_name, sender.last_name),
        MAIL_PORT=465,
        MAIL_SERVER="smtp.mail.ru",
        # "smtp.sendgrid.net"  server domain on which majority of other email domains can be accepted
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
    )
    message = MessageSchema(
        subject="You have a new match!",
        recipients=[recipient.email],
        body=message,
        subtype="plain",
    )
    fm = FastMail(conf)
    await fm.send_message(message)
