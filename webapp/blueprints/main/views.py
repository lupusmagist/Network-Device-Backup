from flask import Blueprint, render_template, request, \
    flash, redirect, url_for, Response
from flask_login import login_required, current_user
from webapp import db
from webapp.models.user import Web_User
from webapp.models.devices import Devices, Backups
from webapp.models.logging import Logging
from webapp.bin.backup import Device_Backup
from webapp.tasks.celery_tasks import send_async_email

main = Blueprint('main', __name__, template_folder='templates',
                 static_folder='static', static_url_path='/main/static')


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/healthy')
def healthy():
    return ('', 200)


@main.route('/home')
@login_required
def home():
    device_list = db.session.query(Devices).all()
    return render_template('main/home.html', devicelist=device_list)


@main.route('/device_add', methods=['GET', 'POST'])
@login_required
def device_add():
    if request.method == 'GET':
        return render_template('main/device_add.html')
    elif request.method == 'POST':
        f_name = request.form.get('name')
        f_ipaddress = request.form.get('ipaddress')
        f_description = request.form.get('description')
        f_username = request.form.get('username')
        f_password = request.form.get('password')
        f_sshport = request.form.get('sshport')
        f_conn_type = request.form.get('type')

        # if this returns a device, then the ip already exists in database
        device = db.session.query(Devices).filter_by(
            device_ip=f_ipaddress).first()

        # if a existing device is found witht he same IP,
        # we want to redirect back to device add  page so
        # we can display a error and the user can try again
        if device:
            flash('IP address already exists')
            return redirect(url_for('main.device_add'))
        else:
            # create new device with the form data.
            new_device = Devices(name=f_name,
                                 device_ip=f_ipaddress,
                                 description=f_description,
                                 ssh_port=f_sshport,
                                 conn_type=f_conn_type,
                                 username=f_username,
                                 password=f_password,
                                 disabled=False)

            # add the new device to the database
            db.session.add(new_device)
            db.session.commit()
            return redirect(url_for('main.home'))
    else:
        flash('Action not allowed.')
        return render_template('main/device_add.html')


@main.route('/device_modify/<int:id>', methods=['GET', 'POST'])
@login_required
def device_modify(id):
    if request.method == 'GET':
        device = db.session.query(Devices).filter_by(id=id).first()
        return render_template('main/device_modify.html', device=device)
    elif request.method == 'POST':
        f_name = request.form.get('name')
        f_ipaddress = request.form.get('ipaddress')
        f_description = request.form.get('description')
        f_username = request.form.get('username')
        f_password = request.form.get('password')
        f_sshport = request.form.get('sshport')
        f_conn_type = request.form.get('type')
        f_state = request.form.get('state')

        if f_state == "1":
            f_state = True
        else:
            f_state = False

        # if this returns a device, then the ip already exists in database
        device = db.session.query(Devices).filter_by(id=id).first()

        device.name = f_name
        device.device_ip = f_ipaddress
        device.description = f_description
        device.ssh_port = f_sshport
        device.username = f_username
        device.password = f_password
        device.conn_type = f_conn_type
        device.disabled = f_state

        db.session.commit()
        return redirect(url_for('main.home'))

    else:
        flash('Action not allowed.')
        return render_template('main/device_modify.html')


@main.route('/device_delete/<int:id>')
@login_required
def device_delete(id):
    db.session.query(Devices).filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('main.home'))


@main.route('/device_backup/<int:did>')
@login_required
def device_backup(did):
    device = db.session.query(Devices).filter_by(id=did).first()
    backup = Device_Backup(device.device_ip,
                           device.username,
                           device.password,
                           device.ssh_port,
                           device.conn_type)
    # print(backup)
    if backup == -1:
        flash('No backup was made, please check logs.')
        return redirect(url_for('main.backup_list', did=did))
    else:
        new_backup = Backups(device_id=device.id,
                             filename=device.name,
                             filedata=backup)

        db.session.add(new_backup)
        db.session.commit()
        return redirect(url_for('main.backup_list', did=did))


@main.route('/backup_list/<int:did>', methods=['GET'])
@login_required
def backup_list(did):
    device = db.session.query(Devices).filter_by(id=did).first()
    backup_list = db.session.query(Backups).all()
    return render_template('main/backup_list.html',
                           backuplist=backup_list, device=device)


@main.route('/backup_get/<int:bid>', methods=['GET'])
@login_required
def backup_get(bid):
    # Returns a file
    backup = db.session.query(Backups).filter_by(id=bid).first()
    return Response(
        backup.filedata,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=" + backup.filename + ".txt"})


@main.route('/backup_delete/<int:did>/<int:bid>')
@login_required
def backup_delete(did, bid):
    db.session.query(Backups).filter_by(id=bid).delete()
    db.session.commit()
    return redirect(url_for('main.backup_list', did=did))


@main.route('/logs_view')
@login_required
def logs_view():
    log_list = db.session.query(Logging).all()
    return render_template('main/logs_view.html', loglist=log_list)


@main.route('/logs_delete')
@login_required
def logs_delete():
    db.session.query(Logging).delete()
    db.session.commit()
    flash('All logs deleted.')
    return redirect(url_for('main.logs_view'))


@main.route('/logs_mail', methods=['GET'])
@login_required
def logs_mail():
    log_list = db.session.query(Logging).all()
    User = db.session.query(Web_User).filter_by(id=current_user.id).first()
    # user_email = User.email
    # send the email
    # email = current_app

    # msg = Message("Logs from the Device Backup system",
    #              recipients=[User.email])
    # msg.body = 'Please find attahced your backup logs as requested.'
    # msg.html = render_template('main/mail_logs.html', loglist=log_list)
    html = render_template('main/mail_logs.html', loglist=log_list)
    email_data = {
        'subject': 'Logs from the Device Backup system',
        'to': User.email,
        'body': html
    }

    send_async_email.delay(email_data)

    flash('Sending email to {0}'.format(User.email))
    return render_template('main/logs_view.html', loglist=log_list)
