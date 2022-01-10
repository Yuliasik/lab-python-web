from flask import Blueprint

categories = Blueprint('category', __name__)

from . import api
