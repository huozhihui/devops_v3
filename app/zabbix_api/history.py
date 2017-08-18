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


if __name__ == '__main__':
    import item, history, datetime

    results = item.filter(itemid=140392)
    print results
    for res in results:
        print res.itemid, res.value_type, res.delay
        his = history.get(res.itemid, res.value_type)
        for h in his:
            dateArray = datetime.datetime.fromtimestamp(float(h.clock))
            dt = dateArray.strftime("%Y-%m-%d %H:%M:%S")
            print dt, h.clock, h.value, h.ns
