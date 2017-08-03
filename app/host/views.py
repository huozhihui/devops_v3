#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, request, session, flash, url_for, redirect, jsonify
from flask_login import login_required

from . import host
from .. import zabbix_api
from forms import HostForm
from ..models import Host
from .. import db


@host.route('/index', methods=['GET'])
@login_required
def index():
    header = u'管理'
    objects = Host.query.all()
    return _render('index', locals())


# 将zabbix服务器主机数据存入本地
@host.route('/ajax_update_data', methods=['GET'])
@login_required
def ajax_update_data():
    try:
        objects = zabbix_api.host.get()
        msg, code = u"更新完成!", 200
    except Exception, e:
        print e
        msg, code = u'更新失败, Zabbix服务器连接失败。', 500
    return jsonify({'msg': msg, 'code': code})


@host.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    header = u'添加'
    form = HostForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if Host.query.filter_by(ip=form.ip.data).first():
                flash(u'IP: {}已存在, 添加失败!'.format(form.ip.data), 'danger')
                return _render('form', locals())

            host = Host(username=form.username.data,
                        password=form.password.data,
                        ip=form.ip.data,
                        port=form.port.data,
                        notes=form.notes.data)
            db.session.add(host)
            try:
                db.session.commit()
                flash(u'主机{}添加成功!'.format(host.ip))
                return redirect(url_for('.index'))
            except Exception, e:
                flash(u'主机{}添加失败, 请联系管理员!'.format(host.ip), 'danger')
                print e.message
                db.session.rollback()
    return _render('form', locals())


@host.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    header = u'编辑'
    obj = Host.query.get_or_404(id)
    form = HostForm(obj=obj)
    if form.validate_on_submit():
        form.populate_obj(obj)
        flash(u'主机{}编辑成功!'.format(obj.ip))
        return redirect(url_for(".index"))
    return _render("edit", locals())


@host.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    obj = Host.query.get(id)
    db.session.delete(obj)
    db.session.commit()
    flash(u'数据删除成功!')
    return redirect(url_for('.index'))


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
    kwargs.update(title_name=u'主机')
    html = "host/%s.html" % content
    return render_template(html, **kwargs)
