#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, request, session, flash, url_for, redirect, jsonify
from flask_login import login_required

import json
from . import cmp
from .. import zabbix_api
from forms import CmpForm
from ..models import Cmp, HostGroup, Inventory, Host
from .. import db

MODULE_NAME = u"监控模版"

@cmp.route('/index', methods=['GET'])
@login_required
def index():
    header = u'管理'
    objects = Cmp.query.all()
    return _render('index', locals())


# 将zabbix服务器主机组数据存入本地
# @host_group.route('/ajax_update_group', methods=['GET'])
# @login_required
# def ajax_update_group():
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
#         msg, code = u"更新完成!", 200
#     except Exception, e:
#         print e
#         msg, code = u'更新失败, Zabbix服务器连接失败。', 500
#     return jsonify({'msg': msg, 'code': code})
#
#
@cmp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    header = u'添加'
    form = CmpForm()
    select_groups = HostGroup.query.all()
    if request.method == "POST":
        if form.validate_on_submit():
            cmp_name = form.name.data
            cmp_groupid = int(request.form.group)
            cmp_hostid = int(request.form.host)
            cmp_notes = form.notes.data
            if Cmp.query.filter_by(name=cmp_name).first():
                flash(u'模版{}已存在, 添加失败!'.format(cmp_name), 'danger')
                return _render('form', locals())

            cmp = Cmp(name=cmp_name,
                      groupid=cmp_groupid,
                      hostid=cmp_hostid,
                      notes=form.notes.data
                      )
            db.session.add(cmp)
            try:
                db.session.commit()
                flash(u'模版{}添加成功!'.format(cmp.name))
                return redirect(url_for('.index'))
            except Exception, e:
                flash(u'模版{}添加失败, 请联系管理员!'.format(cmp_name), 'danger')
                print e.message
                db.session.rollback()
    return _render('form', locals())


# 获取主机列表
@cmp.route('/ajax_get_hosts/<int:id>', methods=['GET'])
@login_required
def ajax_get_hosts(id):
    objects = HostGroup.query.get(id).hosts
    objects = Host.query.all()
    return _render('_host_option', locals())


# #
# @host_group.route('/edit/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit(id):
#     header = u'主机组编辑'
#     obj = HostGroup.query.get_or_404(id)
#     form = HostGroupForm(obj=obj)
#     if form.validate_on_submit():
#         group_name = form.name.data
#         exist_host_group = HostGroup.query.filter_by(name=group_name).first()
#         if exist_host_group and exist_host_group.id != obj.id:
#             flash(u'组名称: {}已存在, 保存失败!'.format(group_name), 'danger')
#         else:
#             form.populate_obj(obj)
#             flash(u'主机组{}编辑成功!'.format(obj.name))
#             return redirect(url_for(".index"))
#     return _render("edit", locals())
#
#
# @host_group.route('/delete/<int:id>', methods=['GET'])
# @login_required
# def delete(id):
#     obj = HostGroup.query.get(id)
#     db.session.delete(obj)
#     db.session.commit()
#     flash(u'数据删除成功!')
#     return redirect(url_for('.index'))
#
#
def _render(content, kwargs={}):
    new_header = MODULE_NAME + kwargs.get('header', '')
    kwargs.update(title_name=MODULE_NAME, header=new_header)
    html = "cmp/%s.html" % content
    return render_template(html, **kwargs)
