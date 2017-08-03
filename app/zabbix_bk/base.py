#!/usr/bin/python
# -*- coding: utf-8 -*-
import functools
from pyzabbix import ZabbixAPI
import setting

def zabbix_connection():
    zabbix_server_ip = setting.SERVER_IP
    zabbix_server_url = setting.SERVER_URL
    zabbix_port = setting.PORT
    zabbix_username = setting.USERNAME
    zabbix_password = setting.PASSWORD

    zapi = ZabbixAPI(zabbix_server_url, timeout=5)
    zapi.login(zabbix_username, zabbix_password)
    return zapi

    # try:
    #     zapi = ZabbixAPI(zabbix_server_url, timeout=10)
    #     zapi.login(zabbix_username, zabbix_password)
    # except Exception, e:
    #     zapi = None
    #     print "Zabbix Server: {}:{} connection timed out!".format(zabbix_server_ip, zabbix_port)
    #     print e.message
    # return zapi

# zapi = zabbix_connection()

# 判断zabbix server是否连接成功的方法
def check_zapi(func):
    functools.wraps(func)
    def wrapper(*args, **kwargs):
        # zapi = zabbix_connection()
        if zapi is None:
            return []
            # return {'result': {}, 'error': 'Zabbix Server connection timed out!'}
        else:
            return func(*args, **kwargs)

    return wrapper


# 基类, 转换zabbix返回的数据
class Base(object):
    def __init__(self, data):
        self.data = data
        if isinstance(self.data, dict):
            self.__dict__.update(**self.data)



