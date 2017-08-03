#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from . import celery_manage
from .. import celery
import time
import json
from flask_socketio import emit
from .. import socketio




@celery_manage.route('/spend_time', methods=['GET', 'POST'])
@login_required
def spend_time():
    print ("耗时的任务")
    # result = send_email.apply_async('zhangsan')  # 变化在这里
    result = send_email.delay('zhangsan')
    print result
    print result.get()
    return render_template('celery_manage/index.html')

# 测试celery
@celery.task
def send_email(name):
    for i in range(2):
        print i
        time.sleep(1)
    # return json.dumps(dict(data=[name, 'world']))
    return name, 'world'
    # return (name, 'world')

# @socketio.on('connect_event')
# def send_ws(name):
#     print "dddddddddd"
#     emit('celery_result', {'data': name})
#     print "fffffffffff"



