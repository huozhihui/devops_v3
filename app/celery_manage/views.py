#!/usr/bin/python
# -*- coding: utf-8 -*-
from .. import celery
from .. import zabbix_api, db
from ..models import Inventory, InventoryUpdate, HostGroup
from collections import OrderedDict
import json
from datetime import datetime
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


# 首先导入inventory
@celery.task(name='import_zabbix_data')
def import_zabbix_data():
    logger.info(u"开始导入主机数据......")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        import_inventory_data()
        logger.info(u"{} 从Zabbix中导入主机数据成功!".format(now))
    except Exception, e:
        logger.error(u"{} 从Zabbix中导入主机数据失败!".format(now))
        logger.error(e.message)

    try:
        import_hostgroup_inventory()
        logger.info(u"{} 从Zabbix中导入主机与组关联数据成功!".format(now))
    except Exception, e:
        logger.error(u"{} 从Zabbix中导入主机与组关联数据失败!".format(now))
        logger.error(e.message)


# 首先导入inventory
# @celery.task(name='import_inventory_data')
def import_inventory_data():
    results = zabbix_api.host.get_inventory()
    for res in results:
        # 如果资产信息不存在, 则跳过
        if not res.inventory:
            continue

        inventory = Inventory.query.filter_by(hostid=res.hostid).first()
        field_dict = match_zabbix_fields()

        res_inventory = res.inventory[0]
        if inventory:
            change_fields = OrderedDict()
            for field, field2 in field_dict.items():
                if field == 'name':
                    res_inventory_field = res.host
                else:
                    res_inventory_field = res_inventory[field2]
                if inventory[field] != res_inventory_field:
                    change_fields[field] = [inventory[field], res_inventory_field]
                    # 更新inventory表数据
                    setattr(inventory, field, res_inventory_field)

            # 保存变更资产记录
            if change_fields:
                content = json.dumps(change_fields)
                inventory_update = InventoryUpdate(inventory_id=inventory.id, content=content)
                db.session.add(inventory_update)
        else:
            insert_data = dict(hostid=res.hostid)
            for field, field2 in field_dict.items():
                insert_data[field] = res_inventory[field2]
            inventory = Inventory(**insert_data)
            db.session.add(inventory)
    db.session.commit()


# 通过本地inventory的hostid导入hostgroup与inventory关系, 同时也导入hostgroup
# @celery.task(name='import_hostgroup_inventory')
def import_hostgroup_inventory():
    inventorys = Inventory.query.all()
    hostids = [obj.hostid for obj in inventorys]
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


# 导入hostgroup
# def import_hostgroup_data():
#     try:
#         results = zabbix_api.hostgroup.get()
#         for res in results:
#             obj = HostGroup.query.filter_by(groupid=res.groupid).first()
#             if obj:
#                 if obj.name != res.name:
#                     obj.name = res.name
#             else:
#                 hostgroup = HostGroup(name=res.name, groupid=res.groupid)
#                 db.session.add(hostgroup)
#         db.session.commit()
#         print "从Zabbix中导入主机组数据成功!"
#         return True
#     except Exception, e:
#         print e
#         print "从Zabbix中导入主机组数据失败!"
#         return False


# 对接zabbix资产信息字段
def match_zabbix_fields():
    fields = ["name", "alias", "type", "asset_tag", "os", "os_short", "os_digits", "os_full",
              "mac_address", "serial_no", "host_networks", "host_netmask", "host_router",
              "oob_ip", "oob_netmask", "oob_router", "date_hw_purchase", "date_hw_install",
              "date_hw_expiry", "date_hw_decomm", "location", "notes"]
    field_dict = OrderedDict()
    for key in fields:
        field_dict[key] = key
    field_dict.update(
        dict(name="host", os_digits="software", mac_address="macaddress_a", serial_no="serialno_a"))
    return field_dict
