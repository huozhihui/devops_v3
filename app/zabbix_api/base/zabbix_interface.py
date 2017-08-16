#!/usr/bin/python
# -*- coding: utf-8 -*-
from . import Base


class ZabbixInterface(Base):
    def __init__(self, data):
        super(ZabbixInterface, self).__init__(data)
        # hostid: 主机ID, 唯一, 必填
        # dns: DNS
        # ip: ip
        # main: # 是否当前默认IP
        #     0 - not default;
        #     1 - default.
        # port: 端口
        # type: 类型
        #     1 - agent;
        #     2 - SNMP;
        #     3 - IPMI;
        #     4 - JMX.
        # useip: Whether the connection should be made via IP.
        #     0 - connect using host DNS name;
        #     1 - connect using host IP address.

