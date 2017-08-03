#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, request, session, flash, redirect, url_for
from flask_login import login_required
from datetime import datetime
import os
import json
import random
import ruamel.yaml
from ruamel.yaml.util import load_yaml_guess_indent
from collections import defaultdict
from ..plugins.playbook_api import run_playbook

from . import task
from forms import TaskForm
from ..models import Homework, Component, Task, Host, Variable
from .. import db


@task.route('/homework_index/', methods=['GET'])
@login_required
def homework_index():
    homework_id = session.get('homework_id')
    if homework_id:
        homework = Homework.query.get(homework_id)
        objects = homework.tasks
        header = u'%s-任务列表' % homework.name
    else:
        flash(u'请首先选择作业!')
        return redirect(url_for('homework.index'))
    return _render('homework_index', locals())


# @task.route('/index/<int:id>', methods=['GET'])
# @login_required
# def index(id):
#     header = u'列表'
#     objects = []
#     return _render('index', locals())


@task.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    header = u'任务编排'
    form = TaskForm()
    homeworks = Homework.query.all()
    components = Component.query.all()
    # 当继续添加的时候,默认为上一个作业
    homework_id = session.get('homework_id')
    if request.method == "POST":
        homework_id = int(request.form.get('type'))
        components = request.form.getlist('component')
        if form.validate_on_submit():
            if not components:
                flash(u'请选择组件', 'danger')
                return _render('form', locals())

            # 如果作业为空,则自动生成作业名称
            if homework_id == 0:
                name = datetime.now().strftime('%Y%m%d%H%M%S')
                homework = Homework(name=name)
                db.session.add(homework)
                db.session.flush()
                homework_id = homework.id
            else:
                homework_id = request.form.get('type')

            # 保存任务
            task = Task(homework_id=homework_id)
            db.session.add(task)
            db.session.flush()

            # 保存对应组件
            for c in components:
                component = Component.query.get(int(c))
                task.components.append(component)
                db.session.add(task)

            try:
                db.session.commit()
                flash(u'任务保存成功!')
                session['homework_id'] = homework_id
            except Exception, e:
                print e.message
                db.session.rollback()
                flash(u'保存失败, 请联系管理员!', 'danger')
            return redirect(url_for('.new'))

    return _render('form', locals())


@task.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    obj = []
    page_header = u"作业编辑"
    print locals()
    return _render('form', locals())


@task.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    obj = Task.query.get(id)
    db.session.delete(obj)
    db.session.commit()
    flash(u'数据删除成功!')
    return redirect(url_for('.homework_index'))


# 配置变量和主机
@task.route('/configure/<int:id>', methods=['GET'])
@login_required
def configure(id):
    task = Task.query.get(id)
    hosts = Host.query.all()
    components = task.components
    c_ids = [c.id for c in components]
    variables = Variable.query.filter(Variable.component_id.in_(c_ids)).all()

    # 编辑时用到
    select_host_ids = [h.id for h in task.hosts]
    if task.variables:
        variables_dict = json.loads(task.variables)

    return _render('dialog_configure', locals())


# 保存任务的主机和变量配置
@task.route('/save_configure/', methods=['POST'])
@login_required
def save_configure():
    host_ids = request.form.getlist('hosts')
    task_id = int(request.form.get('task_id'))

    task = Task.query.get(task_id)
    components = task.components
    c_ids = [c.id for c in components]
    variables = Variable.query.filter(Variable.component_id.in_(c_ids)).all()
    var = defaultdict(dict)
    for v in variables:
        var[v.component.name][v.name] = request.form.get(str(v.id))

    # 保存变量到task表
    task.variables = json.dumps(var)
    # 保存所选主机到关联表时,先清除已选择的主机
    task.hosts = []
    db.session.commit()
    for hid in host_ids:
        host = Host.query.get(int(hid))
        task.hosts.append(host)
        db.session.add(task)
        db.session.commit()

    return redirect(url_for('task.homework_index'))


# 执行任务
@task.route('/execute/<int:id>', methods=['GET'])
@login_required
def execute(id):
    task = Task.query.get(id)
    host_ips = task.get_ips().split(',')
    components = task.components

    now = datetime.now().strftime('%Y%m%d%H%M%S')
    rand = random.randint(0, 99)
    uuid = "%s-%s" % (now, rand)
    # 判断目录是否存在
    uuid = "20170720113901-62"
    uuid_path = os.path.join('/tmp', uuid)
    for component in components:
        for d in ['tasks', 'vars', 'files', 'templates']:
            path = os.path.join(uuid_path, component.name, d)
            if not os.path.exists(path):
                os.makedirs(path)
            if d == 'tasks':
                main_yml = os.path.join(path, 'main.yml')
                with open(main_yml, 'wb') as f:
                    f.write((component.content).encode('utf-8'))
                    f.write('\n')
                # playbook_list.append(main_yml)

            if d == 'vars':
                variables_dict = json.loads(task.variables)
                main_yml = os.path.join(path, 'main.yml')
                with open(main_yml, 'w') as f:
                    for key, value in variables_dict[component.name].items():
                        line = "%s: %s\n" % (key, value)
                        f.write(line)

    # 生成hosts文件
    host_path = os.path.join(uuid_path, 'hosts')
    with open(host_path, 'w') as f:
        f.write('[Task]\n')
        for host in task.hosts:
            s = "{ip} ansible_ssh_user={user} ansible_ssh_pass={password} ansible_ssh_port={port} ansible_connection=ssh\n"
            line = s.format(ip=host.ip, user=host.username, password=host.password, port=host.port)
            f.write(line)

    # 生成入口文件
    with open('./cache/task.yml', 'r') as f:
        config, ind, bsi = load_yaml_guess_indent(f)
    config[0]['hosts'] = 'Task'
    config[0]['roles'] = [c.name for c in task.components]
    role_path = os.path.join(uuid_path, 'task.yml')
    with open(role_path, 'w') as f:
        ruamel.yaml.round_trip_dump(config, f, indent=ind, block_seq_indent=bsi)

    playbook_list = [role_path]
    print host_path
    print playbook_list
    code, result = run_playbook(host_path, playbook_list)
    print code
    print result.host_ok
    print result.host_failed
    print result.host_unreachable

    return redirect(url_for('task.homework_index'))


def _render(content, kwargs={}):
    html = "task/%s.html" % content
    kwargs.update(title_name=u'任务')
    return render_template(html, **kwargs)
