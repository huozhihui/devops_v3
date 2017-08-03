#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, request, session, flash, redirect, url_for
from flask_login import login_required

import os
import random
import time
import json
import tempfile
from datetime import datetime
from ..plugins import ansible_api
from . import script_manage
from forms import ScriptForm
from ..models import ScriptManage, ScriptVariable, Host
from .. import db


@script_manage.route('/index', methods=['GET'])
@login_required
def index():
    header = u'脚本列表'
    objects = ScriptManage.query.all()
    return _render('index', locals())


@script_manage.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    header = u"脚本添加"
    form = ScriptForm()
    if request.method == "POST":
        if form.validate_on_submit():
            script_manage = ScriptManage(name=form.name.data,
                                         type=form.type.data,
                                         content=form.content.data,
                                         notes=form.notes.data
                                         )
            db.session.add(script_manage)
            db.session.flush()
            save_variable(request, script_manage)
            try:
                db.session.commit()
                flash(u'脚本添加成功!')
                return redirect(url_for('.index'))
            except Exception, e:
                flash(u'脚本添加失败, 请联系管理员!', 'danger')
                print e.message
                db.session.rollback()
    return _render('form', locals())


@script_manage.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    header = u'脚本编辑'
    obj = ScriptManage.query.get_or_404(id)
    # 编辑时动态变量框用到
    input_values = [[v.name, v.notes] for v in obj.variables]
    form = ScriptForm(obj=obj)
    if request.method == "POST":
        if form.validate_on_submit():
            form.populate_obj(obj)
            save_variable(request, obj)
            flash(u'脚本编辑成功!')
            return redirect(url_for(".index"))
    return _render("form", locals())


@script_manage.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    obj = ScriptManage.query.get(id)
    db.session.delete(obj)
    db.session.commit()
    flash(u'数据删除成功!')
    return redirect(url_for('.index'))


# 脚本执行页面
@script_manage.route('/execute/<int:id>', methods=['GET', 'POST'])
@login_required
def execute(id):
    hosts = Host.query.all()
    script_manage = ScriptManage.query.get_or_404(id)
    header = script_manage.name
    # if request.method == "POST":
    #     host_id = int(request.form['hosts'])
    #     ip = Host.query.get_or_404(host_id).ip
    return _render("execute", locals())


# 调用ansible,执行任务后返回结果
@script_manage.route('/ajax_execute_task/<int:id>', methods=['GET', 'POST'])
@login_required
def ajax_execute_task(id):
    script_manage = ScriptManage.query.get_or_404(id)
    select_host_ids = json.loads(request.form['hosts'])
    ips = []
    for hid in select_host_ids:
        ips.append(Host.query.get(int(hid)).ip)

    # 获取页面变量,并插入到脚本中
    content_arr = create_script_content(script_manage)

    # 写入脚本文件
    if script_manage.type == "sh":
        temp = tempfile.NamedTemporaryFile(suffix='.sh', prefix='script_', dir='/tmp',)
        try:
            for c in content_arr:
                temp.write("%s\n" % c)
            temp.seek(0)
            # 调用ansible
            code, response = ansible_api.run(ips, 'script', temp.name)
            results = response.result or {}
            print code
            print response.result
        except Exception, e:
            print e.message
            flash(u"写入脚本失败!", 'danger')
        finally:
            pass
            # 关闭并自动删除临时脚本
            # temp.close()

    return _render('_execute_result', locals())


# ajax方式动态增加组件变量
@script_manage.route('/ajax_add_var_tr/<int:i>', methods=['GET', 'POST'])
@login_required
def ajax_add_var_tr(i):
    return _render('_var_tr', locals())


# 保存变量
def save_variable(request, script_manage):
    var_names = request.form.getlist("var_name[]")
    var_values = request.form.getlist("var_value[]")
    # 保存前,先清除相关变量
    script_manage.variables.delete()

    counter = 0
    for var in var_names:
        counter += 1
        if not var:
            continue
        note = var_values[counter - 1]
        variable = ScriptVariable(name=var, notes=note, script_manage_id=script_manage.id)
        db.session.add(variable)


# 创建脚本
# def create_script(script_manage):
#     now = datetime.now().strftime('%Y%m%d%H%M%S')
#     rand = random.randint(0, 99)
#     uuid = "%s-%s" % (now, rand)
#     uuid_path = os.path.join('/tmp', uuid)
#     script_name = "scirpt.%s" % script_manage.type
#     path = os.path.join(uuid_path, script_name)
#     os.makedirs(path)
#     return path


# 将页面变量加入到脚本行数组中
def create_script_content(script_manage):
    content_arr = []
    if script_manage.type == "sh":
        content_arr = script_manage.content.split('\r\n')

    count = 0
    for var in script_manage.variables:
        count += 1
        line = "%s=%s" % (var.name, request.form[var.name])
        content_arr.insert(count, line)

    return content_arr


def _render(content, kwargs={}):
    html = "script_manage/%s.html" % content
    kwargs.update(title_name=u'脚本管理')
    return render_template(html, **kwargs)
