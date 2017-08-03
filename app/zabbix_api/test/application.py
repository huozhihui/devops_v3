#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
from zabbix_api import application


class TestZabbixApplicationApi(unittest.TestCase):
    @unittest.skip('skip get.')
    def test_get(self):
        result = application.get()
        for res in result:
            print res.applicationid, res.name

    # @unittest.skip('skip get hosts.')
    def test_get_items(self):
        result = application.get_items()
        for res in result:
            print res.applicationid, res.name
            print res.items
            for item in res.items:
                print "监控ID: {} 监控名: {}".format(item.hostid, item.name)


if __name__ == '__main__':
    unittest.main()
