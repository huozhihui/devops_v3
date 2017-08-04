#!/usr/bin/python
# -*- coding: utf-8 -*-
from base import login_zabbix
from base import ZabbixHost, ZabbixHostGroup, ZabbixApplication, ZabbixItem, ZabbixInventory


# 获取所有主机
@login_zabbix
def get(**kwargs):
    zapi = kwargs.get('zapi')
    kwargs.pop('zapi', None)

    kwargs.update(output="extend")

    result = []
    try:
        data = zapi.host.get(**kwargs)
        for d in data:
            result.append(ZabbixHost(d))
    except Exception, e:
        print e.message
    return result


# 根据属性获取主机
def filter(**kwargs):
    return get(filter=kwargs)

# 获取资产信息
def get_inventory(**kwargs):
    result = get(filter=kwargs, selectInventory="extend")
    for host in result:
        if isinstance(host.inventory, dict):
            temp = [ZabbixInventory(host.inventory)]
            host.inventory = temp
    return result

# 获取主机组
def get_groups(**kwargs):
    result = get(filter=kwargs, selectGroups="extend")
    for host in result:
        temp = [ZabbixHostGroup(data) for data in host.groups]
        host.groups = temp
    return result


# 获取主机应用集
def get_applications(**kwargs):
    result = get(filter=kwargs, selectApplications="extend")
    for host in result:
        temp = [ZabbixApplication(data) for data in host.applications]
        host.applications = temp
    return result


#  获取主机监控项
def get_items(id):
    result = get(filter={'hostid': id}, selectItems="extend")
    for host in result:
        temp = [ZabbixItem(data) for data in host.items]
        host.items = temp
    return result
