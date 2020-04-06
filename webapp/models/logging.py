from webapp import db
from datetime import datetime


class Logging(db.Model):
    """
    Model for keeping backups.
    """
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_time = db.Column(
        db.DateTime, default=datetime.now, index=True)
    log = db.Column(db.String(200))
    log_type = db.Column(db.String(10))
