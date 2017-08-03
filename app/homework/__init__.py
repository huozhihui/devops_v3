from flask import Blueprint

homework = Blueprint('homework', __name__)

from . import views