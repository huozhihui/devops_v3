#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from . import celery_manage
from .. import celery
import time
import json
from collections import OrderedDict
from flask_socketio import emit
from .. import socketio
from .. import zabbix_api
from ..models import HostGroup, Inventory, InventoryUpdate
from .. import db


@celery_manage.route('/spend_time', methods=['GET', 'POST'])
@login_required
def spend_time():
    print ("耗时的任务")
    # result = send_email.apply_async('zhangsan')  # 变化在这里
    result = send_email.delay('zhangsan')
    print result
    print result.get()
    return render_template('celery_manage/index.html')


# 测试celery
@celery.task
def send_email(name):
    for i in range(2):
        print i
        time.sleep(1)
    # return json.dumps(dict(data=[name, 'world']))
    return name, 'world'
    # return (name, 'world')


# 导入hostgroup
def import_hostgroup_data():
    try:
        results = zabbix_api.hostgroup.get()
        for res in results:
            obj = HostGroup.query.filter_by(groupid=res.groupid).first()
            if obj:
                if obj.name != res.name:
                    obj.name = res.name
            else:
                hostgroup = HostGroup(name=res.name, groupid=res.groupid)
                db.session.add(hostgroup)
        db.session.commit()
        print "从Zabbix中导入主机组数据成功!"
        return True
    except Exception, e:
        print e
        print "从Zabbix中导入主机组数据失败!"
        return False


# 导入inventory
def import_inventory_data():
    try:
        results = zabbix_api.host.get_inventory()
        for res in results:
            obj = Inventory.query.filter_by(hostid=res.hostid).first()
            field_dict = match_zabbix_fields()

            if obj:
                if res.inventory:
                    change_fields = OrderedDict()
                    inventory_data = res.inventory[0]
                    for key, value in field_dict.items():
                        if obj[key] != inventory_data[value]:
                            change_fields[key] = [obj[key], inventory_data[value]]
                            # 更新表数据
                            setattr(obj, key, inventory_data[value])
                    # 保存变更资产记录
                    content = json.dumps(change_fields)
                    inventory_update = InventoryUpdate(inventory_id=obj.id, content=content)
                    db.session.add(inventory_update)
            else:
                if res.inventory:
                    inventory_data = res.inventory[0]
                    insert_data = dict(hostid=res.hostid)
                    for key, value in field_dict.items():
                        insert_data[key] = inventory_data[value]
                    inventory = Inventory(**insert_data)
                    db.session.add(inventory)
        db.session.commit()
        print "从Zabbix中导入主机数据成功!"
        return True
    except Exception, e:
        print e
        print "从Zabbix中导入主机数据失败!"
        return False


# 对接zabbix资产信息字段
def match_zabbix_fields():
    fields = ["type", "asset_tag", "name", "os", "os_short", "os_digits", "os_full",
              "mac_address", "serial_no", "host_networks", "host_netmask", "host_router",
              "oob_ip", "oob_netmask", "oob_router", "date_hw_purchase", "date_hw_install",
              "date_hw_expiry", "date_hw_decomm", "location", "notes"]
    field_hash = OrderedDict()
    for key in fields:
        field_hash[key] = key
    field_hash.update(dict(os_digits="software", mac_address="macaddress_a", serial_no="serialno_a"))
    return field_hash

# 通过本地inventory的hostid导入hostgroup与inventory关系, 此时也导入hostgroup
def import_hostgroup_inventory():
    inventorys = Inventory.query.all()
    hostids = [obj.hostid for obj in inventorys]
    try:
        results = zabbix_api.host.get_groups(hostid=hostids)
        for res in results:
            for group in res.groups:
                # 导入或更新组
                host_group = HostGroup.query.filter_by(groupid=group.groupid).first()
                if host_group:
                    if host_group.name != group.name:
                        host_group.name = group.name
                else:
                    host_group = HostGroup(name=group.name, groupid=group.groupid)
                    db.session.add(host_group)
                    db.session.flush()
                inventory = Inventory.query.filter_by(hostid=res.hostid).first()
                host_group.hosts.append(inventory)
        db.session.commit()
        print "从Zabbix中导入主机与组关联数据成功!"
        return True
    except Exception, e:
        print e
        print "从Zabbix中导入主机与组关联数据失败!"
        return False
