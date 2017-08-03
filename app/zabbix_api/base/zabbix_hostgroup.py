#!/usr/bin/python
# -*- coding: utf-8 -*-
from . import Base


class ZabbixHostGroup(Base):
    def __init__(self, data):
        super(ZabbixHostGroup, self).__init__(data)
        # name: 组名称
        # groupid: 主机组ID