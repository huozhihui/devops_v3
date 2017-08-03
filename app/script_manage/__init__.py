from flask import Blueprint

script_manage = Blueprint('script_manage', __name__)

from . import views