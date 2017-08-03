#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, session, redirect, url_for, flash, jsonify
from flask_login import login_required
from . import main
from ..zabbix_api import hostgroup, host


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # 获取云平台列表,即主机组
    hostgroups = hostgroup.get()

    # 第二行, 仪表, 核数
    # 第二行, 仪表, 内存

    # 第二行, 仪表, 核数

    # m_total = system_data.memory_total
    # m_used = system_data.memory_used
    # d_total = system_data.disk_total
    # d_used = system_data.disk_used
    return _render('index', locals())

# 获取主机列表
@main.route('/ajax_get_hosts/<int:id>', methods=['GET'])
@login_required
def ajax_get_hosts(id):
    try:
        hosts = hostgroup.get_hosts(groupid=id)[0].hosts
    except Exception, e:
        print e.message
    return _render('_host_select', locals())


# 从redis中读取默认云平台
def get_hostgroup():
    return "OpenStack_RZL"

def get_keystone_data():
    item_name = "Keystone API Server is listening on port"



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