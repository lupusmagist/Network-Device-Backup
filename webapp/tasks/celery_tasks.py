
from webapp import mail
from flask import current_app
from flask_mail import Message
from celery import shared_task


@shared_task
def dummy_task():
    return "OK"


@shared_task
def send_async_email(email_data):
    """Background task to send an email with Flask-Mail."""
    msg = Message(email_data['subject'],
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email_data['to']])
    msg.body = email_data['body']
    mail.send(msg)
