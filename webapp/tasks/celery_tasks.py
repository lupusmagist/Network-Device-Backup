
from webapp import mail, db
from flask import current_app, render_template
from flask_mail import Message
from webapp.bin.backup import Device_Backup
from webapp.models.devices import Devices, Backups
from webapp.models.logging import Logging
from webapp.models.user import Web_User
from datetime import datetime, timedelta
from celery import shared_task
# I have to use shared_task becuase importing app from webapp.celery_app cuases
# the worker to fail to load becuase its trying to import this task file,
# but this task file requires the app (worker) to be running


@shared_task
def dummy_task_1():
    return "OK"


@shared_task
def send_async_email(email_data):
    """Background task to send an email with Flask-Mail."""
    msg = Message(email_data['subject'],
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email_data['to']])
    msg.body = email_data['body']
    mail.send(msg)


@shared_task
def scheduled_backups():
    devices = db.session.query(Devices).filter_by(disabled=False).all()
    for device in devices:
        backup = Device_Backup(device.device_ip,
                               device.username,
                               device.password,
                               device.ssh_port,
                               device.conn_type)
        # print(backup)
        if backup == -1:
            log = Logging(log="Backup failed - " +
                          device.device_ip, log_type="FAIL")
            db.session.add(log)
            db.session.commit()
        else:
            new_backup = Backups(device_id=device.id,
                                 filename=device.name,
                                 filedata=backup)
            log = Logging(log="Backup made for: - " +
                          device.device_ip, log_type="SUCCESS")

            db.session.add(log)
            db.session.add(new_backup)
            db.session.commit()


@shared_task
def scheduled_mails():
    d = datetime.today() - timedelta(7)

    users = db.session.query(Web_User).all()
    logs = db.session.query(Logging).filter(
        Logging.date_time.between(d, datetime.today())).all()

    for user in users:
        html = render_template('main/mail_logs.html', loglist=logs)
        email_data = {
            'subject': 'Logs from the Device Backup system',
            'to': user.email,
            'body': html
        }
        send_async_email(email_data)
