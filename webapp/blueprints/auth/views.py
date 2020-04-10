from flask import Blueprint, render_template, redirect, \
    url_for, request, flash
from werkzeug.security import generate_password_hash
from webapp import db
from webapp.models.user import Web_User
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__, template_folder='templates',
                 static_folder='static', static_url_path='/auth/static')


@auth.route('/login')
def login():
    return render_template('auth/login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # if this returns a user, then the email already exists in database
    user = db.session.query(Web_User).filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to
    # the hashed password in database
    if not user:
        flash('Please check your login details and try again.')
        # if user doesn't exist or password is wrong, reload the page
        return redirect(url_for('.login'))

    if not user.check_password(password):
        flash('Please check your login details and try again.')
        # if user doesn't exist or password is wrong, reload the page
        return redirect(url_for('.login'))

    if user.is_disabled():
        flash('Your account is disabled.')
        # if user doesn't exist or password is wrong, reload the page
        return redirect(url_for('.login'))

    # if the above check passes, then we know the user has the
    # right credentials
    login_user(user, remember=remember)
    # Saving last login time
    user.set_last_login()
    db.session.commit()
    return redirect(url_for('main.home'))


@auth.route('/manage_user')
@login_required
def manage_user():
    # if this returns a user, then the email already exists in database
    users = db.session.query(Web_User).all()
    return render_template('auth/manage_user.html', user_list=users)


@auth.route('/modify_user/<int:id>', methods=['GET', 'POST'])
@login_required
def modify_user(id):

    user = db.session.query(Web_User).filter_by(id=id).first()

    return render_template('auth/modify_user.html', user=user)


@auth.route('/modify_user', methods=['POST'])
@login_required
def modify_user_post():
    user_email = request.form.get('email')
    user_name = request.form.get('name')
    user_id = request.form.get('id')
    user_state = request.form.get('state')
    user_type = request.form.get('type')

    if user_state == "1":
        user_state = True
    else:
        user_state = False

    # print("Form username: " + user_id)
    # print("Form username: " + user_type)

    # if this returns a user, then the email already exists in database
    user = db.session.query(Web_User).filter_by(id=user_id).first()

    # Modify the user with the form data.
    user.name = user_name
    user.email = user_email
    user.disabled = user_state
    user.user_type = user_type

    # print("DB username: " + user.name)
    # print("DB username: " + user.email)
    # print("DB username: " + user.disabled)
    # print("DB username: " + user.user_type)

    db.session.commit()
    return redirect(url_for('auth.modify_user', id=user_id))


@auth.route('/create_user')
@login_required
def create_user():
    return render_template('auth/create_user.html')


@auth.route('/create_user', methods=['POST'])
@login_required
def create_user_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user_type = request.form.get('type')

    # if this returns a user, then the email already exists in database
    user = db.session.query(Web_User).filter_by(email=email).first()

    # if a user is found, we want to redirect back to signup page so
    # user can try again
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.create_user'))

    # create new user with the form data. Hash the password so plaintext
    # version isn't saved.
    new_user = Web_User(email=email, name=name,
                        password=generate_password_hash(password,
                                                        method='sha256'),
                        disabled=False, user_type=user_type)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.manage_user'))


@auth.route('/delete_user/<int:id>')
@login_required
def delete_user(id):

    admin_user_count = db.session.query(
        Web_User).filter_by(user_type="ADMIN").count()

    user = db.session.query(Web_User).get(int(id))

    if user.user_type == 'ADMIN':
        if admin_user_count <= 1:
            flash('The last ADMIN user cant be deleted!')
            return redirect(url_for('auth.modify_user', id=id))
        else:
            db.session.query(Web_User).filter_by(id=id).delete()
            db.session.commit()
    else:
        db.session.query(Web_User).filter_by(id=id).delete()
        db.session.commit()

    return redirect(url_for('auth.manage_user'))


@auth.route('/create_user_success')
@login_required
def create_user_success():
    return render_template('auth/create_user_success.html')


@auth.route('/change_password/<int:id>')
@login_required
def change_password(id):

    user = db.session.query(Web_User).get(int(id))

    return render_template('auth/password.html', user=user)


@auth.route('/password', methods=['POST'])
def password():
    id = request.form.get('id')
    password = request.form.get('password')

    user = db.session.query(Web_User).filter_by(id=id).first()
    user.set_password(password)

    db.session.commit()

    return redirect(url_for('auth.manage_user'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
