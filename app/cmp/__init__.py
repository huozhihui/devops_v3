from flask import Blueprint

cmp = Blueprint('cmp', __name__)

from . import views