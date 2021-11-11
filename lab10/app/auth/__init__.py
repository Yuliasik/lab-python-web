from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder="html")

from . import controller
