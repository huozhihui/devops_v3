#!/usr/bin/python
# -*- coding: utf-8 -*-
# from operator import itemgetter
from base import login_zabbix
from base import ZabbixHostGroup, ZabbixHost


# 获取所有主机组
@login_zabbix
def get(**kwargs):
    zapi = kwargs.get('zapi')
    kwargs.pop('zapi', None)

    kwargs.update(output="extend")

    result = []
    try:
        data = zapi.hostgroup.get(**kwargs)
        for d in data:
            result.append(ZabbixHostGroup(d))
    except Exception, e:
        print e.message
    return result


# 根据属性获取主机组
def filter(**kwargs):
    return get(filter=kwargs)


# 获取主机列表
def get_hosts(**kwargs):
    result = get(filter=kwargs, selectHosts="extend")
    for group in result:
        temp = [ZabbixHost(data) for data in group.hosts]
        group.hosts = temp
    return result