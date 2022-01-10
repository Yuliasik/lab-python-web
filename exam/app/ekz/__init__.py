from flask import Blueprint

goods_bp = Blueprint('ekz_goods', __name__)

from . import goods
