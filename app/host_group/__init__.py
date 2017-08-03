from flask import Blueprint

host_group = Blueprint('host_group', __name__)

from . import views