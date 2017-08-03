#!/usr/bin/python
# -*- coding: utf-8 -*-
from . import Base
# from zabbix_hostgroup import ZabbixHostGroup
# from zabbix_application import ZabbixApplication
# from zabbix_item import ZabbixItem


class ZabbixHost(Base):
    def __init__(self, data):
        super(ZabbixHost, self).__init__(data)
        # host: 主机名, 唯一
        # name: 主机的可见名称,默认是属性host
        # hostid: 主机ID
        # description: 主机描述

        # '''主机组'''
        # self.groups = []
        # groups = data.get('groups', [])
        # for group in groups:
        #     self.items.append(ZabbixHostGroup(group))
        #
        # '''主机应用集'''
        # self.applications = []
        # applications = data.get('applications', [])
        # for application in applications:
        #     self.items.append(ZabbixApplication(application))
        #
        # '''主机监控项'''
        # self.items = []
        # items = data.get('items', [])
        # for item in items:
        #     self.items.append(ZabbixItem(item))

        # # 接口信息
        # self.interfaces = []
        # self.ips = []
        # for d in self.data.get('interfaces', []):
        #     self.interfaces.append(Interface(d))
        #     self.ips.append(d.get('ip', ''))
        #
        # # 定义机器是否启动
        # if self.status == '0':
        #     self.status_name = u'已启用'
        #     self.status_color = 'green'
        # else:
        #     self.status_name = u'已停用'
        #     self.status_color = 'red'
