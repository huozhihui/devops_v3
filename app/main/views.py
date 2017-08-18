#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, request, session, redirect, url_for, flash, jsonify
from flask_login import login_required
from . import main
from ..models import Cmp, CmpItem
from .. import socketio, emit
import time


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # 获取云平台
    cmps = Cmp.query.all()
    if request.method == "POST":
        session['main_cmp_id'] = int(request.form.get('cmp'))
        return redirect(url_for('.index'))

    # 获取各监控项最新参数
    item_data = get_latest_data()

    print item_data
    return _render('index', locals())


# 获取各监控项最新参数
def get_latest_data():
    data = dict()
    if 'main_cmp_id' not in session:
        return data

    cmp = Cmp.query.get(session['main_cmp_id'])
    if cmp:
        cmp_items = cmp.cmp_items.all()
        to_TB = ['ram_used', 'ram_total', 'storage_used', 'storage_total']
        show_line = ['mysql']
        for cmp_item in cmp_items:
            if cmp_item.name in to_TB:
                value = "%0.3f" % (int(cmp_item.value) / 1024.0 ** 4)
            # elif 'mysql' in cmp_item.name:
            #     pass
            else:
                value = cmp_item.value
            data[cmp_item.name] = value
    return data


# websocket方法
@socketio.on('connect_event')
def connected_msg(msg):
    item_data = get_latest_data()
    while True:
        emit('ws_update_page', {'data': item_data})
        time.sleep(5)


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on_error()  # Handles the default namespace
def error_handler(e):
    print "websocket异常: %s" % e


@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    print "websocket异常(mo): %s" % e
    pass


# 获取主机列表
# @main.route('/ajax_get_hosts/<int:id>', methods=['GET'])
# @login_required
# def ajax_get_hosts(id):
#     try:
#         hosts = hostgroup.get_hosts(groupid=id)[0].hosts
#     except Exception, e:
#         print e.message
#     return _render('_host_select', locals())


# 从redis中读取默认云平台
# def get_hostgroup():
#     return "OpenStack_RZL"


# def get_keystone_data():
#     item_name = "Keystone API Server is listening on port"


# @main.route('/config_zabbix', methods=['GET', 'POST'])
# @login_required
# def config_zabbix():
#     header = u'添加Zabbix服务器'
#     # flash(u'Zabbix服务器未配置,请首先配置!', 'danger')
#     return _render('config_zabbix', locals())


def _render(content, kwargs={}):
    if not kwargs.has_key('title_name'):
        kwargs.update(title_name=u'首页')
    html = "main/%s.html" % content
    return render_template(html, **kwargs)
