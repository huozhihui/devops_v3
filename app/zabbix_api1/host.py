#!/usr/bin/python
# -*- coding: utf-8 -*-
import functools
from base import ZabbixHost, zabbix_connection


# 获取指定hostid的主机
# @check_zapi
def get(id=None):
    zapi = zabbix_connection()
    kwargs = {
        'selectInterfaces': 'extend',
        'selectInventory': 'extend',
        # 'selectItems': 'extend',
        # 'selectTriggers': 'extend'
        # 'selectGroups': 'extend'
    }
    if id:
        kwargs.update(filter={'hostid': id})
    data = zapi.host.get(**kwargs)
    # return data
    result = []
    for d in data:
        result.append(ZabbixHost(d))
    return result


if __name__ == '__main__':
    hosts = get()
    # print hosts
    for host in hosts:
    #     print host.status_color, host.status_name
        print host.data
        # print host.hostid
        # print host.inventory
        # if host.inventory:
        #     print host.inventory.os
        # print host.interfaces
        # print host.interfaces[0].ip
        # print host.ips
        #     print host.inventory.data
        #     print host.interfaces.data
