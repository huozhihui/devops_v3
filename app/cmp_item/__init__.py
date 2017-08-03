from flask import Blueprint

cmp_item = Blueprint('cmp_item', __name__)

from . import views