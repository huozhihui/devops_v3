#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
# from app.zabbix_api import hostgroup
from app.zabbix_api import item


class TestZabbixItemApi(unittest.TestCase):
    # 测试获取所有组
    @unittest.skip('skip filter.')
    def test_filter(self):
        # result = item.filter(itemid=238010)
        result = item.filter(name="Keystone API Server is listening on port")
        for res in result:
            print res.itemid, res.name, res.type, res.key_

    @unittest.skip('skip filter.')
    def test_filter_with_hostids(self):
        result = item.filter_with_hostids(10295, name="Keystone API Server is listening on port")
        for res in result:
            print res.itemid, res.name, res.type, res.key_

    def test_is_readable(self):
        # 139774 keystone admin api server is listening on port  35357
        # 139775 keystone admin api server is listening on port 5000
        # 139776 keystone main main server process is runing
        # 212711 keystone admin api server is listening on port  35357
        # 212712 keystone admin server process is running
        data = item.is_readable(139774)
        data = item.is_readable(139775)
        data = item.is_readable(139776)
        data = item.is_readable(212711)
        data = item.is_readable(212712)
        pass

if __name__ == '__main__':
    unittest.main()
