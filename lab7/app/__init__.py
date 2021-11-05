from flask_sqlalchemy import SQLAlchemy
from .app import App
from flask_bcrypt import Bcrypt

app = App().getApp()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from . import controller
