#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, request, session, flash, redirect, url_for
from flask_login import login_required

from . import homework
from forms import HomeworkForm
from ..models import Homework, Component
from .. import db


@homework.route('/index', methods=['GET'])
@login_required
def index():
    header = u'作业管理'
    objects = Homework.query.all()
    return _render('index', locals())


@homework.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    header = u'作业添加'
    form = HomeworkForm()
    if request.method == "POST":
        if form.validate_on_submit():
            homework = Homework(name=form.name.data,
                                notes=form.notes.data)
            db.session.add(homework)
            db.session.commit()
            flash(u'作业{}添加成功!'.format(homework.name))
            return redirect(url_for('.index'))
    return _render('form', locals())


@homework.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    header = u'作业编辑'
    obj = Homework.query.get_or_404(id)
    form = HomeworkForm(obj=obj)
    if form.validate_on_submit():
        form.populate_obj(obj)
        flash(u'作业{}编辑成功!'.format(obj.name))
        return redirect(url_for(".index"))
    return _render("form", locals())


@homework.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    obj = Homework.query.get(id)
    db.session.delete(obj)
    db.session.commit()
    if id == session.get('homework_id'):
        session.pop('homework_id')
    flash(u'数据删除成功!')
    return redirect(url_for('.index'))


# 任务列表
@homework.route('/tasklist/<int:id>', methods=['GET'])
@login_required
def tasklist(id):
    session['homework_id'] = id
    return redirect(url_for('task.homework_index'))


# 任务编排
@homework.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    homeworks = Homework.query.all()
    components = Component.query.all()
    return _render('create_task', locals())


def _render(content, kwargs={}):
    kwargs.update(title_name=u'作业')
    html = "homework/%s.html" % content
    return render_template(html, **kwargs)
