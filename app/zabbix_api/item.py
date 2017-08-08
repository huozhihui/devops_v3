#!/usr/bin/python
# -*- coding: utf-8 -*-
from base import login_zabbix
from base.zabbix_item import ZabbixItem


# 获取所有主机
@login_zabbix
def __get(**kwargs):
    zapi = kwargs.get('zapi')
    kwargs.pop('zapi', None)

    kwargs.update(output="extend")
    # kwargs.update(output="extend", hostids="11027", search={"key_": "system"})

    data = zapi.item.get(**kwargs)
    result = []
    for d in data:
        result.append(ZabbixItem(d))
    return result

# 根据属性获取主机组
def filter(**kwargs):
    if not kwargs:
        raise TypeError("filter() kwargs Can't be empty")
    return __get(filter=kwargs)

# 通过主机Id,获取监控项
def filter_with_hostids(hostids, **kwargs):
    return __get(hostids=hostids, filter=kwargs)

# 判断监控项是否可读
@login_zabbix
def is_readable(itemid, **kwargs):
    # 139884 139775 139776 212711 212712
    zapi = kwargs.get('zapi')
    kwargs.pop('zapi', None)

    result = zapi.item.isreadable(itemid)
    return result



# 根据hostid获取主机
# def get_hostid(hostid):
#     return get(filter={'hostid': hostid})


# 根据host name获取主机
# def get_host(host):
#     return get(filter={'host': host})

# for item in get():
#     print item.hostid, item.itemid, item.name, item.key_



