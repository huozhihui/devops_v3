from flask import Blueprint

zabbix_api = Blueprint('zabbix_api', __name__)

from . import host
from . import trigger