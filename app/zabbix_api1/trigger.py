#!/usr/bin/python
# -*- coding: utf-8 -*-
# from base import check_zapi, zapi, Base
# from base import Base, zabbix_connection
from datetime import datetime
from base import Base, zabbix_connection


# 触发器类
class Trigger(Base):
    def __init__(self, data):
        PRIORITY_NAME = {'0': u'未分类',
                         '1': u'信息',
                         '2': u'警告',
                         '3': u'一般严重',
                         '4': u'严重',
                         '5': u'灾难'}
        PRIORITY_COLOR = {'2': 'warning-bg', '3': 'average-bg', '4': 'high-bg', '5': 'disaster-bg'}
        STATUS_NAME = {'0': u'正常', '1': u'异常'}

        super(Trigger, self).__init__(data)
        self.priority_name = PRIORITY_NAME[self.priority]
        self.priority_color = PRIORITY_COLOR[self.priority]
        self.status_name = STATUS_NAME[self.value]
        self.last_change = datetime.fromtimestamp(float(self.lastchange)).strftime('%Y-%m-%d %H:%M:%S')
        self.host_name = self.hosts[0].get('name')
        self.description = self.description.replace('{HOST.NAME}', self.host_name)

    # 历时
    def up_to_now(self):
        self.now = datetime.now()
        time_diff = self.now - datetime.fromtimestamp(float(self.lastchange))
        day = time_diff.days
        hour = time_diff.seconds // 3600
        minutes = (time_diff.seconds // 60) % 60
        second = time_diff.seconds % 60
        result = []
        if day != 0:
            result.append(u'{}天'.format(day))
        if hour != 0:
            result.append(u'{}时'.format(hour))
        if minutes != 0:
            result.append(u'{}分'.format(minutes))
        if len(result) < 3 and second != 0:
            result.append(u'{}秒'.format(second))
        return ' '.join(result)


# @check_zapi
# def get():
#     zapi = zabbix_connection()
    # if zapi is None:
    #     return []
    # result = zapi.trigger.get(output='extend')
    # return {'result': result}


# 所有报警记录
def problems(id=None, **kwargs):
    zapi = zabbix_connection()
    if id:
        kwargs.update(triggerids=id)
    kwargs.update(
        selectHosts='extend',
        filter={'value': 1},
        sortfield="priority",
        sortorder="DESC"
    )
    data = zapi.trigger.get(**kwargs)
    result = []
    for d in data:
        result.append(Trigger(d))
    return result


if __name__ == '__main__':
    for p in problems():
        print p.hosts
        print p.priority_name
        print p.description
