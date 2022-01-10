from flask import Blueprint

form = Blueprint('forms', __name__, template_folder="html")

from . import controller
