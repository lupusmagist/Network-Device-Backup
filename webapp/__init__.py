from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from flask_mail import Mail
from config.settings import DevelopmentConfig, ProductionConfig, TestingConfig


db = SQLAlchemy()
celery = Celery()
mail = Mail()


def create_app(config):
    """
    Create a Flask application using the app factory pattern.
    We pass in the config that we want to use in the settings file

    :return: Flask app
    """

    # Initialize the app
    # app = Flask(__name__, instance_relative_config=False)
    app = Flask(__name__)

    if config == 'debug' or config == 'DEBUG' or config == 'Debug':
        app.config.from_object(DevelopmentConfig())
        print('Running in debug mode')
    elif config == 'production' or config == 'PRODUCTION' or config == 'Production':
        app.config.from_object(ProductionConfig())
        print('Running in production mode')
    elif config == 'testing' or config == 'TESTING' or config == 'Testing':
        app.config.from_object(TestingConfig())
        print('Running in production mode')
    elif config == '':
        print('Please supply a config mode, debug/production/testing.')

    # init the DB
    db.init_app(app)

    # Celery
    init_celery(app)

    mail.init_app(app)

    # Import the database models
    from webapp.models.user import Web_User
    # from webapp.models.devices import Devices

    # Setup login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # if this returns a user, then the email already exists in database
        # user = session.query(Web_User).get(int(user_id))
        # since the user_id is just the primary key of our user table,
        # use it in the query for the user
        return db.session.query(Web_User).get(user_id)

    from webapp.blueprints.main import main
    from webapp.blueprints.auth import auth
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')

    # Create tables for our models when running normaly
    with app.app_context():
        db.create_all()
        add_default_user()

    return app


def init_celery(app=None):
    app = app or create_app()
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    celery.app = app
    return celery


def add_default_user():
    from webapp.models.user import Web_User
    users = db.session.query(Web_User).all()

    if not users:
        # User table is empty, create a default user
        new_user = Web_User(email="admin@example.com", name="admin",
                            disabled=False)

        # add the new user to the database
        db.session.add(new_user)
        new_user.set_password("password")
        new_user.set_user_type("ADMIN")
        db.session.commit()


if __name__ == '__main__':
    app = create_app('debug')
    app.run('127.0.0.1', 5000, debug='true')
