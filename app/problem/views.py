#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, request, session, flash
from flask_login import login_required
import time
# from flask_socketio import emit
# from .. import socketio

from . import problem
from .. import zabbix_api


@problem.route('/index', methods=['GET'])
@login_required
def index():
    try:
        problems = zabbix_api.trigger.problems()
    except Exception, e:
        print e
        problems = []
        flash(u'zabbix服务端连接失败。', 'danger')
    return _render('index', problems=problems)


# 返回主机信息
def _render(content, **kwargs):
    html = "problem/%s.html" % content
    kwargs.update(title_name=u'监控报警')
    return render_template(html, **kwargs)


# websocket方法
# @socketio.on('connect_event')
def connected_msg(msg):
    problems = zabbix_api.trigger.problems()
    data = []
    priority_color = []
    for pb in problems:
        data.append([
            pb.host_name,
            # pb.priority_color,
            pb.priority_name,
            pb.status_name,
            pb.last_change,
            pb.up_to_now(),
            pb.description
        ])
        priority_color.append(pb.priority_color)
    emit('ws_problem_update_table', {'data': data})
    emit('ws_problem_update_priority_color', {'data': priority_color})

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
#     inventorys = zabbix_api.host.get_inventory(id)
#     return _show_host('_asset_info', inventorys=inventorys)


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
