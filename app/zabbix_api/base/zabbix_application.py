#!/usr/bin/python
# -*- coding: utf-8 -*-
from . import Base


class ZabbixApplication(Base):
    def __init__(self, data):
        super(ZabbixApplication, self).__init__(data)
        # applicationid 模版ID
        # hostid 主机ID
        # name  应用名称
        # templateids 父模版应用的IDs

