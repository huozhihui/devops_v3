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

    @unittest.skip('skip get items.')
    def test_get_items(self):
        hosts = host.get_items(10295)
        # hosts = host.get(filter={'hostid': 11027}, selectItems="extend")
        # for h in hosts:
        #     print h.hostid, h.name, h.items
        # for res in h.items:
        #     print "监控ID: {} 监控名: {} ".format(res.itemid, res.name)

    # @unittest.skip('skip get items.')
    def test_get_inventory(self):
        hosts = host.get_inventory()
        for h in hosts:
            print h.hostid, h.name, h.host
            print "=========================="
            print h.inventory
            for inventory in h.inventory:
                for key, value in inventory.__dict__.items():
                    print "%20s: %s" % (key, value)
                    # inventory = h.inventory[0]
                    # print inventory.data

    @unittest.skip('skip get interfaces.')
    def test_get_interfaces(self):
        hosts = host.get_interfaces()
        for h in hosts:
            print h.hostid, h.name
            for res in h.interfaces:
                info = "IP: {}  DNS: {} Main: {} Port: {} Type: {} Useip: {}"
                print info.format(res.ip, res.dns, res.main, res.port, res.type, res.useip)


if __name__ == '__main__':
    unittest.main()
