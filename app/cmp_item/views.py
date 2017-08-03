#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, request, session, flash, url_for, redirect, jsonify
from flask_login import login_required

from . import cmp_item
from .. import zabbix_api
# from forms import HostGroupForm
from ..models import CmpItem
from .. import db


@cmp_item.route('/index', methods=['GET'])
@login_required
def index():
    header = u'监控项管理'
    objects = CmpItem.query.all()
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
# @host_group.route('/new', methods=['GET', 'POST'])
# @login_required
# def new():
#     header = u'主机组添加'
#     form = HostGroupForm()
#     if request.method == "POST":
#         if form.validate_on_submit():
#             group_name = form.name.data
#             if HostGroup.query.filter_by(name=group_name).first():
#                 flash(u'组名称: {}已存在, 添加失败!'.format(group_name), 'danger')
#                 return _render('form', locals())
#
#             hostgroup = HostGroup(name=group_name)
#             db.session.add(hostgroup)
#             try:
#                 db.session.commit()
#                 flash(u'主机组{}添加成功!'.format(hostgroup.name))
#                 return redirect(url_for('.index'))
#             except Exception, e:
#                 flash(u'主机组{}添加失败, 请联系管理员!'.format(group_name), 'danger')
#                 print e.message
#                 db.session.rollback()
#     return _render('form', locals())
# #
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

def _render(content, kwargs={}):
    kwargs.update(title_name=u'监控项')
    html = "host_group/%s.html" % content
    return render_template(html, **kwargs)
