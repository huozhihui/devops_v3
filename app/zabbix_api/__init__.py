from flask import Blueprint

zabbix_api = Blueprint('zabbix_api', __name__)

from . import hostgroup
from . import host
from . import application
from . import item
from . import history