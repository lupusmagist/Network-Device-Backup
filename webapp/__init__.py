from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from environs import Env

env = Env()
db = SQLAlchemy()


def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.
    We pass in the config that we want to use in the settings file

    :return: Flask app
    """

    # Initialize the app
    app = Flask(__name__, instance_relative_config=False)

    # Load config from file
    env.read_env()
    FLASK_DEBUG = env.bool("FLASK_DEBUG")
    if FLASK_DEBUG:
        app.config.from_object('config.settings.DevelopmentConfig')
        print('running in debug mode')
    else:
        app.config.from_object('config.settings.ProductionConfig')

    # init the DB
    db.init_app(app)

    # Setup login manager
    from webapp.models.user import Web_User
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

    # Create tables for our models
    with app.app_context():
        db.create_all()
        add_default_user()

    return app


def add_default_user():
    from webapp.models.user import Web_User
    users = db.session.query(Web_User).all()

    if not users:
        # User table is empty, create a default user
        new_user = Web_User(email="admin@example.co.za", name="admin",
                            disabled=False)

        # add the new user to the database
        db.session.add(new_user)
        new_user.set_password("password")
        new_user.set_user_type("ADMIN")
        db.session.commit()


if __name__ == '__main__':
    app = create_app()
    app.run('127.0.0.1', 5000, debug=True)
