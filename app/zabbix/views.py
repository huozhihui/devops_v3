#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, request, session, flash, redirect, url_for
from flask_login import login_required

from . import zabbix
from .. import zabbix_api
from ..inventory.forms import InventoryForm


# from forms import ZabbixForm
# from ..models import Zabbix
# from .. import db

# Zabbix主机发现
@zabbix.route('/hosts', methods=['GET'])
@login_required
def hosts():
    header = u'主机发现'
    try:
        objects = zabbix_api.host.get()
    except Exception, e:
        print e
        flash(u'zabbix服务端连接失败。', 'danger')
    return _render('host_index', locals())


# Zabbix主机资产信息
@zabbix.route('/inventory/<int:hostid>', methods=['GET'])
@login_required
def inventory(hostid):
    try:
        host = zabbix_api.host.get(hostid)[0]
        inventory = host.inventory
        form = InventoryForm()
    except Exception, e:
        print e
        flash(u'zabbix服务端连接失败。', 'danger')
        redirect(url_for('.hosts'))
    return _render('host_inventory', locals())  # @zabbix.route('/new', methods=['GET', 'POST'])


# @login_required
# def new():
#     header = u'添加Zabbix服务器'
#     form = ZabbixForm()
# if request.method == "POST":
#     if form.validate_on_submit():
#         homework = Zabbix(name=form.name.data,
#                             notes=form.notes.data)
#         db.session.add(homework)
#         db.session.commit()
#         flash(u'作业{}添加成功!'.format(homework.name))
#         return redirect(url_for('.index'))
#     return _render('form', locals())
#
def _render(content, kwargs={}):
    if not kwargs.has_key('title_name'):
        kwargs.update(title_name=u'Zabbix')
    html = "zabbix/%s.html" % content
    return render_template(html, **kwargs)
