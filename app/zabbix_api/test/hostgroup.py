#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
from zabbix_api import hostgroup


class TestZabbixHostGroupApi(unittest.TestCase):
    # 测试获取所有组
    @unittest.skip('skip get.')
    def test_get(self):
        result = hostgroup.get()
        for res in result:
            print res.groupid, res.name

    # @unittest.skip('skip get hosts.')
    def test_get_hosts(self):
        result = hostgroup.get_hosts()
        for res in result:
            print res.groupid, res.name
            for host in res.hosts:
                print "主机ID: {} 主机名: {}".format(host.hostid, host.name)


if __name__ == '__main__':
    unittest.main()
