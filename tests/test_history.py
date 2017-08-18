#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
# from app.zabbix_api import history, item
# from app.zabbix_api import history, item

# from app import zabbix_api
# from app import zabbix_api
from app import Mail

class TestZabbixHistoryApi(unittest.TestCase):
    pass
    # @unittest.skip('skip get groups.')
    # def test_get(self):
    #     results = zabbix_api.item.filter(itemid=140392)
    #     print results
    #     for res in results:
    #         print res.itemid, res.value_type
        # result = history.get(139841, 0)
        # for his in result:
        #     print "监控ID: {}, 时间: {}, 值: {}, 纳秒: {}".format(his.itemid, his.clock, his.value, his.ns)


if __name__ == '__main__':
    unittest.main()
