from flask import Blueprint

goods = Blueprint('goods', __name__, template_folder="templates")

from . import controller
