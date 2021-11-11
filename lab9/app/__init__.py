from flask_sqlalchemy import SQLAlchemy
from .app import App
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = App().getApp()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from . import controller, models
