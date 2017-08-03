#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, request, session, flash, redirect, url_for
from flask_login import login_required

from .. import db
from . import variable
from forms import VariableForm
from ..models import Component, Variable


@variable.route('/index', methods=['GET'])
@login_required
def index():
    header = u'管理'
    objects = Variable.query.all()
    return _render('index', locals())


@variable.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    header = u'添加'
    form = VariableForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # 保存组件信息
            component = Variable(name=form.name.data,
                                 type=form.type.data,
                                 version=form.version.data,
                                 os=form.os.data,
                                 content=form.content.data,
                                 notes=form.notes.data)
            db.session.add(component)
            db.session.flush()
            db.session.commit()

            flash(u'组件{}添加成功!'.format(component.name))
            return redirect(url_for('.index'))

        else:
            flash(u'表单校验未通过,添加失败!', 'danger')

    return _render('form', locals())


@variable.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    header = u"编辑"
    obj = Variable.query.get_or_404(id)
    form = VariableForm(obj=obj)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(obj)
            flash(u'组件{}编辑成功!'.format(obj.name))
            return redirect(url_for(".index"))
        else:
            flash(u'表单校验未通过,编辑失败!', 'danger')
    return _render('form', locals())


@variable.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    obj = Variable.query.get(id)
    db.session.delete(obj)
    db.session.commit()
    flash(u'数据删除成功!')
    return redirect(url_for('.index'))


def _render(content, kwargs={}):
    kwargs.update(title_name=u'变量')
    html = "variable/%s.html" % content
    return render_template(html, **kwargs)
