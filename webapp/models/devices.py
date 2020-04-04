from webapp import db
from datetime import datetime


class Devices(db.Model):
    """
    Model for keeping devices.
    Set the connection type
        set_conn_type("MIKROTIK")
        supported options: MIKROTIK, HP, UBNTRADIO
    Check connection type
        check_conn_type("MIKROTIK")
        Returns True if connection type is MIKROTIK, False otherwise.
    Check device enable/disabled state:
        is_disabled() returns true or false.
    Enable and disable device:
        set_disabled(True or False)
    """

    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), index=True)
    device_ip = db.Column(db.String(80))
    description = db.Column(db.String(200))
    conn_type = db.Column(db.String(80))
    ssh_port = db.Column(db.Integer)
    username = db.Column(db.String(200))
    password = db.Column(db.String(200))
    disabled = db.Column(db.Boolean)

    def set_conn_type(self, conntype):
        accepted_types = {'MIKROTIK', 'HP', 'UBNTRADIO'}
        if conntype in accepted_types:
            self.conn_type = conntype
        else:
            return -1

    def check_conn_type(self, conntype):
        accepted_types = {'MIKROTIK', 'HP', 'UBNTRADIO'}
        if conntype in accepted_types:
            if conntype == self.conn_type:
                return True
            else:
                return False
        else:
            return -1

    def is_disabled(self):
        return self.disabled

    def set_disabled(self, state):
        self.disabled = state


class Backups(db.Model):
    """
    Model for keeping backups.
    """
    __tablename__ = 'backups'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_id = db.Column(db.Integer)
    filename = db.Column(db.String(80))
    filedata = db.Column(db.String())
    uploaddate = db.Column(
        db.DateTime, default=datetime.now, index=True)
