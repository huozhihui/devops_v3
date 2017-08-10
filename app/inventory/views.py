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
            # tmp_dict['inventory_id'] = inventory.id
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
                    print update_data
                    if update_data:
                        if not save_inventory_update(inventory, update_data):
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


def save_inventory_update(inventory, json_data):
    content = json.dumps(json_data)
    inventory_update = InventoryUpdate(content=content, inventory_id=inventory.id)
    db.session.add(inventory_update)
    print "save inventory_update"
    try:
        db.session.commit()
        return True
    except Exception, e:
        print e.message
        db.session.rollback()
        return False


# 将zabbix服务器主机组数据存入本地
# @inventory.route('/ajax_update_inventory', methods=['GET'])
# @login_required
# def ajax_update_inventory():
#     try:
#         celery_manage.views.import_inventory_data()
#         celery_manage.views.import_hostgroup_inventory()
#         msg, code = u"更新完成!", 200
#     except Exception, e:
#         print e.message
#         msg, code = u'更新失败, 请联系管理员!', 500
#     return jsonify({'msg': msg, 'code': code})


def _render(content, kwargs={}):
    new_header = MODULE_NAME + kwargs.get('header', '')
    kwargs.update(title_name=MODULE_NAME, header=new_header)
    html = "inventory/%s.html" % content
    return render_template(html, **kwargs)
