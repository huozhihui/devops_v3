#!/usr/bin/python
# -*- coding: utf-8 -*-
import functools
from pyzabbix import ZabbixAPI
import setting


# 基类, 转换zabbix返回的数据
class Base(object):
    def __init__(self, data):
        self.data = data
        if isinstance(self.data, dict):
            self.__dict__.update(**self.data)

    def __getitem__(self, item):
        return self.__dict__[item]


from zabbix_host import ZabbixHost
from zabbix_inventory import ZabbixInventory
from zabbix_hostgroup import ZabbixHostGroup
from zabbix_application import ZabbixApplication
from zabbix_item import ZabbixItem
from zabbix_history import ZabbixHistory


# 判断zabbix server是否连接成功的方法
def login_zabbix(func):
    functools.wraps(func)

    def wrapper(*args, **kwargs):
        zabbix_server_url = setting.SERVER_URL
        zabbix_username = setting.USERNAME
        zabbix_password = setting.PASSWORD
        zapi = ZabbixAPI(zabbix_server_url, timeout=30)
        zapi.login(zabbix_username, zabbix_password)
        kwargs.update(zapi=zapi)
        return func(*args, **kwargs)
        # try:
        #     zapi = ZabbixAPI(zabbix_server_url, timeout=30)
        #     zapi.login(zabbix_username, zabbix_password)
        #     print 'Zabbix Server connection is successful!'
        # except Exception, e:
        #     print e.message
        #     print 'Zabbix Server connection timed out!'
        #     zapi = None
        #
        # if zapi is None:
        #     return []
        # else:
        #     kwargs.update(zapi=zapi)
        #     return func(*args, **kwargs)

    return wrapper
