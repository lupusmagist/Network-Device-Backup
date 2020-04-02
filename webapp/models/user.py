from webapp import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import date, datetime

now = datetime.now()


class Web_User(UserMixin, db.Model):
    """
    Model for authenticating users on the web interface.
    Set password for a User:
        set_password(new_password)
        password is automaticly encryted
    Check if given password matches current user password:
        check_password(password)
        returns true or false
    Check User enable/disabled state:
        is_disabled() returns true or false.
    Enable and disable user:
        set_disabled(True or False)
    Record login time/date
        set_last_login()
        No agruments needed.
    Set the user type
        set_user_type("ADMIN")
        supported options: ADMIN, MOD, USER
    Check user type
        check_user_type("ADMIN")
        Returns True if user is a ADMIN, False otherwise.
    """

    __tablename__ = 'web-users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), index=True)
    email = db.Column(db.String(80), index=True)
    password = db.Column(db.String(200))
    disabled = db.Column(db.Boolean)
    created_on = db.Column(db.DateTime, default=date.today, index=True)
    last_login = db.Column(db.String(80))

    # User type: ADMIN, MOD, USER
    user_type = db.Column(db.String(10))

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def set_user_type(self, usertype):
        accepted_types = {'ADMIN', 'MOD', 'USER'}
        if usertype in accepted_types:
            self.user_type = usertype
        else:
            return -1

    def check_user_type(self, usertype):
        accepted_types = {'ADMIN', 'MOD', 'USER'}
        if usertype in accepted_types:
            if usertype == self.user_type:
                return True
            else:
                return False
        else:
            return -1

    def set_last_login(self):
        self.last_login = now.strftime("%m/%d/%Y, %H:%M:%S")

    def is_disabled(self):
        return self.disabled

    def set_disabled(self, state):
        self.disabled = state

    def __repr__(self):
        return '<User {}>'.format(self.name)
