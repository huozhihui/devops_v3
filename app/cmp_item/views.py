#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, request, session, flash, url_for, redirect, jsonify
from flask_login import login_required

from . import cmp_item
from .. import zabbix_api
from forms import CmpItemForm
from ..models import CmpItem, Cmp, Inventory, HostGroup
from .. import db

MODULE_NAME = u"监控项目"


@cmp_item.route('/index', methods=['GET'])
@login_required
def index():
    header = u'管理'
    objects = CmpItem.query.all()
    return _render('index', locals())


# 从监控平台添加项目
@cmp_item.route('/new/<int:id>', methods=['GET', 'POST'])
@login_required
def new(id):
    header = u'添加'
    cmp = Cmp.query.get_or_404(id)
    form = CmpItemForm()
    if request.method == "POST":
        if form.validate_on_submit():
            form_data = dict(hostid=int(request.form.get('host')),
                             applicationid=int(request.form.get('application')),
                             itemid=int(request.form.get('item')),
                             name=form.name.data,
                             notes=form.notes.data
                             )

            # 保存监控平台项目cmp_item表
            form_data['cmp_id'] = cmp.id
            if save_cmp_item(cmp, form_data):
                return redirect(url_for('.new'))

    return _render('form', locals())


@cmp_item.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    header = u'编辑'
    cmp_item = CmpItem.query.get_or_404(id)
    cmp = cmp_item.cmp
    form = CmpItemForm(obj=cmp_item)
    if request.method == "POST":
        if form.validate_on_submit():
            form.hostid.data = int(request.form.get('host'))
            form.applicationid.data = int(request.form.get('application'))
            form.itemid.data = int(request.form.get('item'))
            form.populate_obj(cmp_item)
            flash(u'监控项目{}编辑成功!'.format(cmp_item.name))
            return redirect(url_for(".index"))

            # form_data = dict(hostid=int(request.form.get('host')),
            #                  applicationid=int(request.form.get('application')),
            #                  itemid=int(request.form.get('item')),
            #                  name=form.name.data,
            #                  notes=form.notes.data
            #                  )

            # 保存监控平台项目cmp_item表
            # form_data['cmp_id'] = cmp.id
            # if not save_cmp_item(cmp, form_data):
            #     return _render('new', locals())

    return _render('form', locals())


# 获取主机列表
@cmp_item.route('/ajax_get_hosts/<int:id>', methods=['GET'])
@login_required
def ajax_get_hosts(id):
    try:
        objects = HostGroup.query.get(id).hosts
        msg, code = _render('_host_option', locals()), 200
    except Exception, e:
        print e
        msg, code = "获取主机失败!", 500
    return jsonify({'msg': msg, 'code': code})


# 获取应用集列表
@cmp_item.route('/ajax_get_applications/<int:host_id>', methods=['GET'])
@login_required
def ajax_get_applications(host_id):
    hostid = Inventory.query.get_or_404(host_id).hostid
    try:
        objects = zabbix_api.host.get_applications(hostid=hostid)[0].applications
        msg, code = _render('_application_option', locals()), 200
    except Exception, e:
        print e
        msg, code = "获取应用集失败!", 500
    return jsonify({'msg': msg, 'code': code})


# 获取监控项列表
@cmp_item.route('/ajax_get_items/<int:applicationid>', methods=['GET'])
@login_required
def ajax_get_items(applicationid):
    try:
        objects = []
        result_items = zabbix_api.application.get_items(applicationid)[0].items
        for res in result_items:
            history = zabbix_api.history.get(res.itemid, res.value_type)
            if len(history) > 0:
                objects.append(res)
        if len(objects) == 0:
            msg, code = "可用监控项为空!", 300
        else:
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


# 从监控项目添加项目
@cmp_item.route('/fast_new', methods=['GET', 'POST'])
@login_required
def fast_new():
    header = u'添加'
    form = CmpItemForm()
    select_groups = HostGroup.query.all()
    if request.method == "POST":
        try:
            form.hostid.data = int(request.form.get('host'))
            form.applicationid.data = int(request.form.get('application'))
            form.itemid.data = int(request.form.get('item'))
        except Exception, e:
            print e.message
        if form.validate_on_submit():
            cmp_data = dict(group_id=int(request.form.get('group')))
            cmp_item_data = dict(hostid=form.hostid.data,
                                 applicationid=form.applicationid.data,
                                 itemid=form.itemid.data,
                                 name=form.name.data,
                                 notes=form.notes.data
                                 )

            # 保存监控平台cmp表
            host_group = HostGroup.query.get(cmp_data['group_id'])
            cmp = Cmp.query.filter_by(name=host_group.name).first()
            if not cmp:
                cmp = Cmp(name=host_group.name,
                          groupid=host_group.id,
                          )
                db.session.add(cmp)
                db.session.flush()

            # 保存监控平台项目cmp_item表
            cmp_item_data['cmp_id'] = cmp.id
            if save_cmp_item(cmp, cmp_item_data):
                return redirect(url_for('.fast_new'))
        else:
            flash(u'表单验证失败, 请完善必填项!')

    return _render('fast_new', locals())


# 保存监控项目方法
def save_cmp_item(cmp, data):
    name = data.get('name')
    host_id = data.get('host_id')

    if CmpItem.query.filter_by(name=name, hostid=host_id, cmp_id=cmp.id).first():
        flash(u'监控项目{}已存在, 添加失败!'.format(name), 'danger')
        return False

    cmp_item = CmpItem(**data)
    db.session.add(cmp_item)
    try:
        db.session.commit()
        flash(u'监控项目{}添加成功!'.format(name))
        return True
    except Exception, e:
        print e.message
        db.session.rollback()
        flash(u'监控项目{}添加失败, 请联系管理员!'.format(name), 'danger')
        return False


def _render(content, kwargs={}):
    new_header = MODULE_NAME + kwargs.get('header', '')
    kwargs.update(title_name=MODULE_NAME, header=new_header)
    html = "cmp_item/%s.html" % content
    return render_template(html, **kwargs)
