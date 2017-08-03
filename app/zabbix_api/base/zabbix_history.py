#!/usr/bin/python
# -*- coding: utf-8 -*-
from . import Base


class ZabbixHistory(Base):
    def __init__(self, data):
        super(ZabbixHistory, self).__init__(data)
        # clock: 时间
        # itemid: 监控项ID
        # ns: 纳秒
        # value: 值

