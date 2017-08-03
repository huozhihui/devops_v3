#!/usr/bin/python
# -*- coding: utf-8 -*-
from . import Base


class ZabbixItem(Base):
    def __init__(self, data):
        super(ZabbixItem, self).__init__(data)
        # hostid: 主机ID, 唯一, 必填
        # host: 主机名, 唯一
        # name: 监控项名称
        # type: # 监控类型
        # description: 监控描述
        # history: 历史天数
        # key_: 键值
        # status: 状态,
        #     0 - (default) enabled item;
        #     1 - disabled item.
