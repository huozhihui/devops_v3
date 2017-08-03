#!/usr/bin/python
# -*- coding: utf-8 -*-
from base import login_zabbix
from base import ZabbixApplication, ZabbixItem


# 获取应用集
@login_zabbix
def get(**kwargs):
    zapi = kwargs.get('zapi')
    kwargs.pop('zapi', None)

    kwargs.update(output="extend")

    result = []
    try:
        data = zapi.application.get(**kwargs)
        for d in data:
            result.append(ZabbixApplication(d))
    except Exception, e:
        print e.message
    return result


# 根据属性获取应用集
def filter(**kwargs):
    return get(filter=kwargs)


# 获取监控项列表
def get_items(id):
    result = get(filter={'applicationid': id}, selectItems="extend")
    for application in result:
        temp = [ZabbixItem(data) for data in application.items]
        application.items = temp
    return result
