from webapp import db


class Devices(db.Model):
    """
    Model for keeping devices.
    Set the device type
        set_device_type("HP")
        supported options: HP, MIKRO, UBNT
    Check device type
        check_device_type("HP")
        Returns True if device is HP, False otherwise.
    Check device enable/disabled state:
        is_disabled() returns true or false.
    Enable and disable device:
        set_disabled(True or False)

    """

    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), index=True)
    device_type = db.Column(db.String(80))
    device_ip = db.Column(db.String(80))
    username = db.Column(db.String(200))
    password = db.Column(db.String(200))
    command = db.Column(db.String(200))
    disabled = db.Column(db.Boolean)

    def set_device_type(self, devicetype):
        accepted_types = {'HP', 'MIKRO', 'UBNT'}
        if devicetype in accepted_types:
            self.device_type = devicetype
        else:
            return -1

    def check_device_type(self, devicetype):
        accepted_types = {'HP', 'MIKRO', 'UBNT'}
        if devicetype in accepted_types:
            if devicetype == self.device_type:
                return True
            else:
                return False
        else:
            return -1

    def is_disabled(self):
        return self.disabled

    def set_disabled(self, state):
        self.disabled = state
