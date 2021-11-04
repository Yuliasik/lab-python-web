from flask_sqlalchemy import SQLAlchemy
from app.app import App

app = App().getApp()
db = SQLAlchemy(app)

from app import controller
