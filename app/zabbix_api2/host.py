#!/usr/bin/python
# -*- coding: utf-8 -*-
from base import login_zabbix

# 获取主机
@login_zabbix
def host_get(**kwargs):
    zapi = kwargs.get('zapi')
    return zapi.host.get(output="extend")

