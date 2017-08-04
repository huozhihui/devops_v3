#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, request, session, flash, redirect, url_for, jsonify
from flask_login import login_required
import json
from collections import OrderedDict

from . import inventory
from .forms import InventoryForm
from ..models import Host, HostGroup, Inventory, InventoryUpdate
from .. import db
from .. import zabbix_api
from .. import celery_manage

MODULE_NAME = u"主机"


@inventory.route('/index', methods=['GET'])
@login_required
def index():
    header = u'管理'
    objects = Inventory.query.all()
    return _render('index', locals())


@inventory.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    header = u'编辑'
    inventory = Inventory.query.get_or_404(id)
    form = InventoryForm(obj=inventory)
    if request.method == 'POST':
        if form.validate_on_submit():
            tmp_dict = OrderedDict()
            for field, content in form._fields.items():
                tmp_dict[field] = form[field].data
            # tmp_dict = copy.deepcopy(form.data)
            tmp_dict.pop('csrf_token', None)
            tmp_dict.pop('submit', None)
            tmp_dict['inventory_id'] = inventory.id
            if not inventory:
                pass
                # if save_inventory(tmp_dict):
                #     flash(u'主机{}资产信息添加成功!'.format(host.ip))
                #     return redirect(url_for("host.index"))
                # else:
                #     flash(u'主机{}资产信息添加失败,请联系管理员!'.format(host.ip), 'danger')
            else:
                # 如果资产记录存在, 则对比表单提交与数据库中各字段存储数据是否一致
                # 针对不一致的字段,将该字段的名称存储起来, 以便于信息变更的历史查询
                update_data = OrderedDict()
                inventory_dict = inventory.to_dict()
                for key, new_value in tmp_dict.items():
                    old_val = inventory_dict[key]
                    if old_val != new_value:
                        label_name = form[key].label.text
                        update_data[label_name] = [old_val, new_value]
                try:
                    form.populate_obj(inventory)
                    flash(u'主机{}资产信息编辑成功!'.format(inventory.name))
                    if update_data:
                        if not save_inventory_update(update_data):
                            flash(u'主机{}的信息变更存储失败!'.format(inventory.name), 'danger')
                    return redirect(url_for(".index"))
                except Exception, e:
                    print e.message
                    flash(u'主机{}资产信息编辑失败,请联系管理员!'.format(inventory.name), 'danger')

    return _render("edit", locals())


def save_inventory(data):
    try:
        inventory = Inventory(**data)
        db.session.add(inventory)
        db.session.commit()
        return True
    except Exception, e:
        print e.message
        db.session.rollback()
        return False


def save_inventory_update(json_data):
    content = json.dumps(json_data)
    inventory_update = InventoryUpdate(content=content)
    db.session.add(inventory_update)
    try:
        db.session.commit()
        return True
    except Exception, e:
        print e.message
        db.session.rollback()
        return False


# 将zabbix服务器主机组数据存入本地
@inventory.route('/ajax_update_inventory', methods=['GET'])
@login_required
def ajax_update_inventory():
    import_inventory = celery_manage.views.import_inventory_data()
    import_hostgroup_inventory = celery_manage.views.import_hostgroup_inventory()
    if import_inventory and import_hostgroup_inventory:
        msg, code = u"更新完成!", 200
    else:
        msg, code = u'更新失败, 请联系管理员!', 500
    return jsonify({'msg': msg, 'code': code})


# @inventory.route('/edit/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit(id):
#     print "aaaaaaaaaa"
#     header = u'编辑'
#     obj = Inventory.query.get_or_404(id)
#     form = AssetForm(obj=obj)
#     if form.validate_on_submit():
#         pass

# try:
#     host = zabbix.host.get(id)[0]
#     inventory = host.inventory
# except Exception, e:
#     print e
#     host = None
#     inventory = None
#     flash(u'zabbix服务端连接失败。', 'danger')
# return _render("edit", locals())


# 显示主机资产信息
# @inventory.route('/show/<int:id>', methods=['GET'])
# @login_required
# def show(id):
#     host = zabbix.host.get(id)[0]
#     inventory = host.inventory
#     return _render('show', inventory=inventory, host=host)


# 显示主机信息
# @host.route('/show/<int:id>', methods=['GET'])
# @login_required
# def show(id):
#     session['hostid'] = id
#     inventorys = zabbix_api.host.get_inventory(id)
#     return _show_host('show', inventorys=inventorys)


# 显示主机资产信息
# @host.route('/asset_info/<int:id>', methods=['GET'])
# @login_required
# def asset_info(id):
#     inventory = zabbix_api.host.get_inventory(id)[0]
#     return _show_host('_asset_info', inventory=inventory)


# 主机-系统信息
# @host.route('/system_info/<int:id>', methods=['GET'])
# @login_required
# def system_info(id):
#     inventorys = zabbix_api.host.get_inventory(id)
#     return _show_host('_system_info', inventorys=inventorys)


# 主机-问题
# @host.route('/problem_info/<int:id>', methods=['GET'])
# def problem_info(id):
#     problems = zabbix_api.host.get_problem(id)
#     return _show_host('_problem_info', problems=problems)

# problems = zabbix_api.host.get_problem(id)
# priority_name = {'0': u'未分类', '1': u'信息', '2': u'警告', '3': u'一般严重', '4': u'严重', '5': u'灾难'}
# priority_color = {'2': 'warning-bg', '3': 'average-bg', '4': 'high-bg', '5': 'disaster-bg'}
# status = {'0': u'正常', '1': u'异常'}
# problems = zabbix_api.host.get_problem(id)
# host = zabbix_api.host.find_by_id(id)
# host_name = host['name'] or host['host']
# current_time = datetime.utcnow()
# # datetime.fromtimestamp(1497509975).strftime('%Y-%m-%d %H:%M:%S')
# return _show_host('problem_info',
#                   priority_name=priority_name,
#                   rs=problems['result'],
#                   host_name=host_name,
#                   status = status,
#                   priority_color=priority_color,
#                   current_time = current_time,
#                   )

# 主机-问题
# @host.route('/trigger_info/<int:id>', methods=['GET'])
# def trigger_info(id):
#     triggers = zabbix_api.host.get_triggers(id)
#     return _show_host('_trigger_info', triggers=triggers)


def _render(content, kwargs={}):
    new_header = MODULE_NAME + kwargs.get('header', '')
    kwargs.update(title_name=MODULE_NAME, header=new_header)
    html = "inventory/%s.html" % content
    return render_template(html, **kwargs)
