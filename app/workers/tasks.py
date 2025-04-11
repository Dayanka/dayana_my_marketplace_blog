import os
import smtplib
from email.message import EmailMessage
from app.workers.celery_app import celery_app
import logging
from app.config import settings



# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    logger.addHandler(handler)

@celery_app.task
def send_registration_email(email: str):
    from app.config import settings
    SMTP_SERVER = settings.smtp_server
    SMTP_PORT = settings.smtp_port
    SMTP_USER = settings.smtp_user
    SMTP_PASSWORD = settings.smtp_password

    msg = EmailMessage()
    msg["Subject"] = "Регистрация успешно завершена"
    msg["From"] = SMTP_USER
    msg["To"] = email
    msg.set_content("Ваш аккаунт успешно создан!")

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise Exception(f"Error sending email: {e}")

    logger.info(f"Email sent to {email}")
    return f"Email sent to {email}"
