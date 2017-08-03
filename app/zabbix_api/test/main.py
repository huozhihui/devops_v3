#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
from zabbix_api import hostgroup, host, application, history


class TestZabbixApi(unittest.TestCase):
    # 1、获取主机组列表
    @unittest.skip('skip get hostgroup.')
    def test_hostgroup(self):
        groups = hostgroup.get()
        for g in groups:
            print g.groupid, g.name

    # 2、通过主机组id=34,获取主机列表
    @unittest.skip('skip get hosts.')
    def test_hosts(self):
        try:
            hosts = hostgroup.get_hosts(groupid=34)[0].hosts
        except Exception, e:
            print e.message
            hosts = []
        for host in hosts:
            print host.hostid, host.name

    # 3、通过主机id=10295, 获取应用集列表
    @unittest.skip('skip get application.')
    def test_applications(self):
        try:
            applications = host.get_applications(hostid=10295)[0].applications
        except Exception, e:
            print e.message
            applications = []

        for ap in applications:
            print ap.applicationid, ap.name

    # 4、通过应用集id=1644 name=Capacity data, 获取监控列表
    @unittest.skip('skip get items.')
    def test_items(self):
        try:
            items = application.get_items(1644)[0].items
        except Exception, e:
            print e.message
            items = []

        for it in items:
            print "监控ID: {}, 名称: {}, 值类型: {}".format(it.itemid, it.name, it.value_type)

    # 5、根据监控项id=[139841, 139842], 获取监控最新值
    @unittest.skip('skip get history.')
    def test_history(self):
        historys = []
        for itemid, value_type in [(139841, 3), (139842, 3)]:
            historys.append(history.get(itemid, value_type)[0])
        # try:
        #     historys = history.get([139841, 139842], 3)
        # except Exception, e:
        #     print e.message
        #     historys = []

        for his in historys:
            print "监控ID: {}, 时间: {}, 值: {}, 纳秒: {}".format(his.itemid, his.clock, his.value, his.ns)


    # 获取CPU核数
    def test_cpu_core(self):
        pass
if __name__ == '__main__':
    unittest.main()
