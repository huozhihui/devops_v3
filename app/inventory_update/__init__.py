from flask import Blueprint

inventory_update = Blueprint('inventory_update', __name__)

from . import views