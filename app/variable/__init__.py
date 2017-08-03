from flask import Blueprint

variable = Blueprint('variable', __name__)

from . import views