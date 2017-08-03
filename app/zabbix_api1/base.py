#!/usr/bin/python
# -*- coding: utf-8 -*-
from pyzabbix import ZabbixAPI
import setting

# 基类, 转换zabbix返回的数据
class Base(object):
    def __init__(self, data):
        self.data = data
        if isinstance(self.data, dict):
            self.__dict__.update(**self.data)


# 资产类
class Inventory(Base):
    def __init__(self, data):
        super(Inventory, self).__init__(data)


# 接口类
class Interface(Base):
    pass


class ZabbixHost(Base):
    def __init__(self, data):
        super(ZabbixHost, self).__init__(data)
        if data.get('inventory'):
            self.inventory = Inventory(data.get('inventory'))

        # 接口信息
        self.interfaces = []
        self.ips = []
        for d in self.data.get('interfaces', []):
            self.interfaces.append(Interface(d))
            self.ips.append(d.get('ip', ''))

        # 定义机器是否启动
        if self.status == '0':
            self.status_name = u'已启用'
            self.status_color = 'green'
        else:
            self.status_name = u'已停用'
            self.status_color = 'red'


def zabbix_connection():
    zabbix_server_ip = setting.SERVER_IP
    zabbix_server_url = setting.SERVER_URL
    zabbix_port = setting.PORT
    zabbix_username = setting.USERNAME
    zabbix_password = setting.PASSWORD

    zapi = ZabbixAPI(zabbix_server_url, timeout=5)
    zapi.login(zabbix_username, zabbix_password)
    return zapi


'''
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
'''
