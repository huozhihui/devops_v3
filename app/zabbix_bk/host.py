#!/usr/bin/python
# -*- coding: utf-8 -*-
# from base import zapi, check_zapi, Base
from base import Base, zabbix_connection


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
        for d in self.data.get('interfaces'):
            self.interfaces.append(Interface(d))
            self.ips.append(d.get('ip', ''))

        # 定义机器是否启动
        if self.status == '0':
            self.status_name = u'已启用'
            self.status_color = 'green'
        else:
            self.status_name = u'已停用'
            self.status_color = 'red'


# 获取指定hostid的主机
# @check_zapi
def get(id=None):
    zapi = zabbix_connection()
    # if zapi is None:
    #     return []
    kwargs = {
        'selectInterfaces': 'extend',
        'selectInventory': 'extend'
    }
    if id:
        kwargs.update(filter={'hostid': id})
    data = zapi.host.get(**kwargs)
    result = []
    for d in data:
        result.append(ZabbixHost(d))
    return result


if __name__ == '__main__':
    hosts = get()
    for host in hosts:
        print host.hostid
        # print host.inventory
        # if host.inventory:
        #     print host.inventory.os
        print host.interfaces
        print host.interfaces[0].ip
        print host.ips
        #     print host.inventory.data
        #     print host.interfaces.data
