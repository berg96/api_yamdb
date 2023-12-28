import smtplib
import random
import os

from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

sender_email = os.getenv('SENDER_EMAIL')
password = os.getenv('PASSWORD')


def generate_verification_code():
    return str(random.randint(1000, 9999))


def send_verification_email(recipient_email, verification_code):
    msg = EmailMessage()
    msg['Subject'] = 'Код подтверждения'
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg.set_content(f'Ваш код подтверждения: {verification_code}')

    with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as server:
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
