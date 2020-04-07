""" Settings File """
from datetime import timedelta
from webapp import env


class Config:
    """ Global config class for app
    Use python-dotenv to import private settings from .env file
    """

    APP_NAME = 'Device Manager'

    SECRET_KEY = '1q2w3e4r5'

    # Celery.
    CELERY_BROKER_URL = 'redis://redis:6379/0'
    CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_REDIS_MAX_CONNECTIONS = 5
    CELERY_TIMEZONE = "UTC"

    # User.
    SEED_ADMIN_EMAIL = 'dev@local.host'
    SEED_ADMIN_PASSWORD = 'devpassword'
    REMEMBER_COOKIE_DURATION = timedelta(days=90)

    # Flask-Mail configuration
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = env.str('MAIL_USERNAME')
    MAIL_PASSWORD = env.str('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'flask@example.com'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1q2w3e4r5@database/DM'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
