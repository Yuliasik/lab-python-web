from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import config
from flask import Flask
from flask_migrate import Migrate
from .app import App

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()

login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    app.api_login = config.get(config_name).API_LOGIN
    app.api_password = config.get(config_name).API_PASSWORD

    with app.app_context():
        from . import controller

        from .auth import auth
        app.register_blueprint(auth, url_prefix='/auth')

        from .forms import form
        app.register_blueprint(form, url_prefix='/forms')

        from .posts import posts
        app.register_blueprint(posts, url_prefix='/posts')

        from .categories_api import categories
        app.register_blueprint(categories, url_prefix='/api/categories')

        return app
