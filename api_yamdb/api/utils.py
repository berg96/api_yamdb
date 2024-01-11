import smtplib
import random
import os

from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
PASSWORD = os.getenv('PASSWORD')


def generate_verification_code():
    return str(random.randint(1000, 9999))


def send_verification_email(recipient_email, verification_code):
    msg = EmailMessage()
    msg['Subject'] = 'Код подтверждения'
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg.set_content(f'Ваш код подтверждения: {verification_code}')

    with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()
