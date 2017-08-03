#!/usr/bin/python
# -*- coding: utf-8 -*-
import functools
from pyzabbix import ZabbixAPI
import setting


# def login_zabbix():
#     zabbix_server_url = setting.SERVER_URL
#     zabbix_username = setting.USERNAME
#     zabbix_password = setting.PASSWORD
#     zapi = ZabbixAPI(zabbix_server_url, timeout=5)
#     zapi.login(zabbix_username, zabbix_password)
#     return zapi

# 判断zabbix server是否连接成功的方法
def login_zabbix(func):
    functools.wraps(func)

    def wrapper(*args, **kwargs):
        zabbix_server_url = setting.SERVER_URL
        zabbix_username = setting.USERNAME
        zabbix_password = setting.PASSWORD
        zapi = ZabbixAPI(zabbix_server_url, timeout=5)
        zapi.login(zabbix_username, zabbix_password)
        if zapi is None:
            return []
            # return {'result': {}, 'error': 'Zabbix Server connection timed out!'}
        else:
            kwargs.update(zapi=zapi)
            return func(*args, **kwargs)

    return wrapper
