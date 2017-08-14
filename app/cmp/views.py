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

MODULE_NAME = u"监控平台"


@cmp.route('/index', methods=['GET'])
@login_required
def index():
    header = u'管理'
    objects = Cmp.query.all()
    return _render('index', locals())


@cmp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    header = u'添加'
    form = CmpForm()
    select_groups = HostGroup.query.all()
    if request.method == "POST":
        if form.validate_on_submit():
            form_data = dict(name=form.name.data,
                             groupid=int(request.form.get('group')),
                             notes=form.notes.data
                             )

            if not save_cmp(form_data):
                return _render('form', locals())

            try:
                db.session.commit()
                flash(u'监控平台{}添加成功!'.format(form_data['name']))
                return redirect(url_for('.index'))
            except Exception, e:
                flash(u'监控平台{}添加失败, 请联系管理员!'.format(form_data['name']), 'danger')
                print e.message
                db.session.rollback()
    return _render('form', locals())


@cmp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    header = u'编辑'
    select_groups = HostGroup.query.all()
    cmp = Cmp.query.get_or_404(id)
    form = CmpForm(obj=cmp)
    if form.validate_on_submit():
        cmp_name = form.name.data
        cmp_groupid = int(request.form.get('group'))
        cmp_notes = form.notes.data
        exist_cmp = Cmp.query.filter_by(name=cmp_name).first()
        if exist_cmp and exist_cmp.id != cmp.id:
            flash(u'监控平台{}已存在, 保存失败!'.format(cmp_name), 'danger')
            return _render('form', locals())
        else:
            cmp.groupid = cmp_groupid
            form.populate_obj(cmp)
            flash(u'监控平台{}编辑成功!'.format(cmp.name))
            return redirect(url_for(".index"))
    return _render("form", locals())


@cmp.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    obj = Cmp.query.get_or_404(id)
    db.session.delete(obj)
    db.session.commit()
    flash(u'数据删除成功!')
    return redirect(url_for('.index'))


# 保存监控项目方法
def save_cmp(data):
    name = data.get('name')
    if Cmp.query.filter_by(name=name).first():
        flash(u'监控平台{}已存在, 添加失败!'.format(name), 'danger')
        return False

    cmp = Cmp(**data)
    db.session.add(cmp)
    return True


def _render(content, kwargs={}):
    new_header = MODULE_NAME + kwargs.get('header', '')
    kwargs.update(title_name=MODULE_NAME, header=new_header)
    html = "cmp/%s.html" % content
    return render_template(html, **kwargs)
