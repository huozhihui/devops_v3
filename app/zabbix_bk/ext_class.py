#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from collections import OrderedDict
import pdb


class Base(object):
    def __init__(self, dict):
        self.data = dict
        for k, v in dict.items():
            setattr(self, k, v)
            self.zh_attribute(k)

    # 增加属性翻译方法
    def zh_attribute(self, attr):
        attr_zh = "{}_zh".format(attr)
        self.__dict__.update({attr_zh: self.zh(attr)})

    # 子类需重构
    def zh(self, attr):
        return attr


class Host(Base):
    def __init__(self, dict):
        super(Host, self).__init__(dict)
        # 定义机器是否启动
        if self.status == '0':
            self.status_name = u'已启用'
            self.status_color = 'green'
        else:
            self.status_name = u'已停用'
            self.status_color = 'red'

        self.inventory = Inventory(self.inventory)


class Inventory(Base):
    def __init__(self, dict):
        super(Inventory, self).__init__(dict)

    def zh(self, attr):
        zh_dict = {'type': u"类型"}
        return zh_dict.get(attr, attr)



class Trigger(Base):
    def __init__(self, dict):
        self.data = dict
        self.triggers = self.data['triggers'] or [{}]
        # self.host_name = self.data['name'] or self.data['host']
        print self.triggers
        if self.triggers:
            for k, v in self.triggers[0].items():
                setattr(self, k, v)


class Problem(Base):
    def __init__(self, dict):
        PRIORITY_NAME = {'0': u'未分类',
                         '1': u'信息',
                         '2': u'警告',
                         '3': u'一般严重',
                         '4': u'严重',
                         '5': u'灾难'}
        PRIORITY_COLOR = {'2': 'warning-bg', '3': 'average-bg', '4': 'high-bg', '5': 'disaster-bg'}
        STATUS_NAME = {'0': u'正常', '1': u'异常'}

        super(Problem, self).__init__(dict)
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


        # def __str__(self):
        #     return self.dict
        #
        # def __unicode__(self):
        #     return self.value
