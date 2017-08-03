from flask import Blueprint

component = Blueprint('component', __name__)

from . import views