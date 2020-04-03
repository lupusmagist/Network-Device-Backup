from webapp import db


class Devices(db.Model):
    """
    Model for keeping devices.
    Set the connection type
        set_conn_type("SSH")
        supported options: SSH, TELNET
    Check connection type
        check_conn_type("SSH")
        Returns True if connection type is SSH, False otherwise.
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
    username = db.Column(db.String(200))
    password = db.Column(db.String(200))
    command = db.Column(db.String(200))
    disabled = db.Column(db.Boolean)

    def set_conn_type(self, conntype):
        accepted_types = {'SSH', 'TELNET'}
        if conntype in accepted_types:
            self.conn_type = conntype
        else:
            return -1

    def check_conn_type(self, conntype):
        accepted_types = {'SSH', 'TELNET'}
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
