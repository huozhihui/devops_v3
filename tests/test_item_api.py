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

    def test_filter_with_hostids(self):
        result = item.filter_with_hostids(10295, name="Keystone API Server is listening on port")
        for res in result:
            print res.itemid, res.name, res.type, res.key_


if __name__ == '__main__':
    unittest.main()
