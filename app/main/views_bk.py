#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, session, redirect, url_for, flash
from flask_login import login_required
from . import main
from .forms import NameForm
from .. import db
from ..models import User
import psutil as ps
from .. import system_data


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # return redirect(url_for('zabbix.new'))
    # 第二行, 仪表, 内存
    m_total = system_data.memory_total
    m_used = system_data.memory_used
    d_total = system_data.disk_total
    d_used = system_data.disk_used
    return _render('index', locals())

# @main.route('/config_zabbix', methods=['GET', 'POST'])
# @login_required
# def config_zabbix():
#     header = u'添加Zabbix服务器'
#     # flash(u'Zabbix服务器未配置,请首先配置!', 'danger')
#     return _render('config_zabbix', locals())


def _render(content, kwargs={}):
    if not kwargs.has_key('title_name'):
        kwargs.update(title_name=u'首页')
    html = "main/%s.html" % content
    return render_template(html, **kwargs)


# @main.route('/', methods=['GET', 'POST'])
# @login_required
# def index():
#     title_name = '首页'
#     form = NameForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.name.data).first()
#         if user is None:
#             user = User(username=form.name.data)
#             db.session.add(user)
#             session['known'] = False
#         else:
#             session['known'] = True
#         session['name'] = form.name.data
#         form.name.data = ''
#         return redirect(url_for('.index'))
#     return render_template('index.html',
#                            form=form, name=session.get('name'),
#                            known=session.get('known', False),
#                            current_time=datetime.utcnow())
