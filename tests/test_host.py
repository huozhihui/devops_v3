#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
from app.zabbix_api import host

class TestZabbixHostApi(unittest.TestCase):
    # 测试获取主机组
    @unittest.skip('skip get groups.')
    def test_get_groups(self):
        result = host.get_groups()
        for res in result:
            print res.hostid, res.name
            for group in res.groups:
                print "组ID: {} 组名: {} ".format(group.groupid, group.name)

    @unittest.skip('skip get applications.')
    def test_get_applications(self):
        hosts = host.get_applications()
        for h in hosts:
            print h.hostid, h.name
            for res in h.applications:
                print "应用ID: {} 应用名: {} ".format(res.applicationid, res.name)

    # @unittest.skip('skip get items.')
    def test_get_items(self):
        hosts = host.get_items(10295)
        # hosts = host.get(filter={'hostid': 11027}, selectItems="extend")
        # for h in hosts:
        #     print h.hostid, h.name, h.items
            # for res in h.items:
            #     print "监控ID: {} 监控名: {} ".format(res.itemid, res.name)



if __name__ == '__main__':
    unittest.main()
