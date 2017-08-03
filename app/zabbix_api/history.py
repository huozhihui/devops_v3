#!/usr/bin/python
# -*- coding: utf-8 -*-
from base import login_zabbix
from base.zabbix_history import ZabbixHistory


# 获取所有主机, 需要监控ID和该监控数值类型
@login_zabbix
def get(itemid, value_type, **kwargs):
    zapi = kwargs.get('zapi')
    kwargs.pop('zapi', None)

    kwargs.update(output="extend",
                  itemids=itemid,
                  history=value_type,
                  sortfield="clock",
                  sortorder="DESC",
                  limit=1
                  )

    result = []
    try:
        data = zapi.history.get(**kwargs)
        for d in data:
            result.append(ZabbixHistory(d))
    except Exception, e:
        print e.message
    return result