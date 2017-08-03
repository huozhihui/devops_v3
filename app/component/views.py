#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, request, session, flash, redirect, url_for, current_app
from flask_login import login_required
import json
import os
from werkzeug.utils import secure_filename

# from ..base import _render
from . import component
from forms import ComponentForm
from ..models import Component, UploadFile, Variable
from .. import db


@component.route('/index', methods=['GET'])
@login_required
def index():
    header = u'管理'
    objects = Component.query.all()
    return _render('index', locals())

# 显示变量列表
@component.route('/variable_index/<int:id>', methods=['GET'])
@login_required
def variable_index(id):
    title_name = u'变量'
    header = u'管理'
    component = Component.query.get_or_404(id)
    objects = component.variables.all()
    return _render('variable_index', locals())

# 显示文件列表
@component.route('/file_index/<int:id>', methods=['GET'])
@login_required
def file_index(id):
    title_name = u'文件'
    header = u'管理'
    component = Component.query.get_or_404(id)
    objects = component.upload_files.all()
    return _render('file_index', locals())


@component.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    header = u'添加'
    form = ComponentForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # 保存组件信息
            component = Component(name=form.name.data,
                                  type=form.type.data,
                                  version=form.version.data,
                                  os=form.os.data,
                                  content=form.content.data,
                                  notes=form.notes.data)
            db.session.add(component)
            db.session.flush()

            # 保存变量
            save_variable(request, component)

            # 保存上传的文件
            files = request.files.getlist("files[]")
            templates = request.files.getlist("templates[]")

            # 轮询上传过来的文件保存到指定文件夹及数据库
            for file in files:
                save_upload_file(file, 'file', component)

            for file in templates:
                save_upload_file(file, 'template', component)

            # 将组件及上传文件信息提交到数据库
            db.session.commit()

            flash(u'组件{}添加成功!'.format(component.name))
            return redirect(url_for('.index'))

        else:
            flash(u'表单校验未通过,添加失败!', 'danger')

    return _render('form', locals())


@component.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    header = u"编辑"
    obj = Component.query.get_or_404(id)
    form = ComponentForm(obj=obj)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(obj)
            # 保存变量
            save_variable(request, obj)

            # 保存上传的文件
            files = request.files.getlist("files[]")
            templates = request.files.getlist("templates[]")

            # 轮询上传过来的文件保存到指定文件夹及数据库
            for file in files:
                filename = secure_filename(file.filename)
                save_upload_file(file, 'type', obj)

            for file in templates:
                save_upload_file(file, 'type', obj)

            # 将组件及上传文件信息提交到数据库
            db.session.commit()
            flash(u'组件{}编辑成功!'.format(obj.name))
            return redirect(url_for(".index"))
        else:
            flash(u'表单校验未通过,编辑失败!', 'danger')
    return _render('form', locals())


@component.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    obj = Component.query.get(id)
    db.session.delete(obj)
    db.session.commit()
    flash(u'数据删除成功!')
    return redirect(url_for('.index'))


# ajax方式动态增加组件变量
@component.route('/ajax_add_var_tr/<int:i>', methods=['GET', 'POST'])
@login_required
def ajax_add_var_tr(i):
    return _render('_var_tr', locals())


# 保存变量
def save_variable(request, component):
    var_names = request.form.getlist("var_name[]")
    var_values = request.form.getlist("var_value[]")
    counter = 0
    for var in var_names:
        counter += 1
        if not var:
            continue
        value = var_values[counter - 1]
        type = request.form['var_type_%s' % counter]
        variable = Variable(name=var, value=value, type=type, component_id=component.id)
        db.session.add(variable)


# 保存上传文件
def save_upload_file(file, type, component):
    if file:
        upload_path = current_app.config['UPLOAD_FOLDER']
        filename = secure_filename(file.filename)
        save_path = os.path.join(upload_path, component.name)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        file.save(os.path.join(upload_path, component.name, filename))
        upload_file = UploadFile(name=filename,
                                 path=component.name,
                                 type=type,
                                 component_id=component.id
                                 )
        db.session.add(upload_file)


def _render(content, kwargs={}):
    if not kwargs.has_key('title_name'):
        kwargs.update(title_name=u'组件')
    html = "component/%s.html" % content
    return render_template(html, **kwargs)
