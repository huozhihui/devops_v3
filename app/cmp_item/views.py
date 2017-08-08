#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, request, session, flash, url_for, redirect, jsonify
from flask_login import login_required

from . import cmp_item
from .. import zabbix_api
from forms import CmpItemForm
from ..models import CmpItem, Cmp, Inventory
from .. import db

MODULE_NAME = u"监控项目"


@cmp_item.route('/index', methods=['GET'])
@login_required
def index():
    header = u'管理'
    objects = CmpItem.query.all()
    return _render('index', locals())


@cmp_item.route('/new/<int:id>', methods=['GET', 'POST'])
@login_required
def new(id):
    header = u'添加'
    cmp = Cmp.query.get_or_404(id)
    form = CmpItemForm()
    if request.method == "POST":
        if form.validate_on_submit():
            print request.form
            name = form.name.data
            application_id = int(request.form.get('application'))
            item_id = int(request.form.get('item'))
            notes = form.notes.data
            if CmpItem.query.filter_by(name=name, cmp_id=cmp.id).first():
                flash(u'监控项目{}已存在, 添加失败!'.format(name), 'danger')
                return _render('form', locals())

            cmp_item = CmpItem(name=name,
                               applicationid=application_id,
                               itemid=item_id,
                               notes=notes,
                               cmp_id=cmp.id)
            db.session.add(cmp_item)
            try:
                db.session.commit()
                flash(u'监控项目{}添加成功!'.format(cmp_item.name))
                # return redirect(url_for('.index'))
            except Exception, e:
                flash(u'监控项目{}添加失败, 请联系管理员!'.format(name), 'danger')
                print e.message
                db.session.rollback()
    return _render('form', locals())


# 获取应用集列表
@cmp_item.route('/ajax_get_applications/<int:cmp_id>', methods=['GET'])
@login_required
def ajax_get_applications(cmp_id):
    cmp = Cmp.query.get_or_404(int(cmp_id))
    hostid = Inventory.query.get_or_404(int(cmp.hostid)).hostid
    try:
        objects = zabbix_api.host.get_applications(hostid=hostid)[0].applications
        msg, code = _render('_application_option', locals()), 200
    except Exception, e:
        print e
        msg, code = "获取应用集失败!", 500
    return jsonify({'msg': msg, 'code': code})


# 获取监控项列表
@cmp_item.route('/ajax_get_items/<int:application_id>', methods=['GET'])
@login_required
def ajax_get_items(application_id):
    try:
        objects = []
        result_items = zabbix_api.application.get_items(application_id)[0].items
        for res in result_items:
            history = zabbix_api.history.get(res.itemid, res.value_type)
            if len(history) > 0:
                objects.append(res)
        msg, code = _render('_item_option', locals()), 200
    except Exception, e:
        print e
        msg, code = "获取监控项失败!", 500
    return jsonify({'msg': msg, 'code': code})


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
@cmp_item.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    obj = CmpItem.query.get(id)
    db.session.delete(obj)
    db.session.commit()
    flash(u'数据删除成功!')
    return redirect(url_for('.index'))


def _render(content, kwargs={}):
    new_header = MODULE_NAME + kwargs.get('header', '')
    kwargs.update(title_name=MODULE_NAME, header=new_header)
    html = "cmp_item/%s.html" % content
    return render_template(html, **kwargs)
