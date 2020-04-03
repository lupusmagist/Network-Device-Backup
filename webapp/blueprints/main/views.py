from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from webapp import db
from webapp.models.devices import Devices

main = Blueprint('main', __name__, template_folder='templates',
                 static_folder='static', static_url_path='/main/static')


@main.route('/')
def index():
    return render_template('main/index.html')


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
        f_command = request.form.get('command')
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
                                 command=f_command,
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
        f_command = request.form.get('command')
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
        device.command = f_command
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


@main.route('/device_backup')
@login_required
def device_backup():
    device_list = db.session.query(Devices).all()
    return render_template('main/home.html', devicelist=device_list)
