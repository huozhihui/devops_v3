#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Length


# 定义表单类
class ZabbixForm(FlaskForm):
    ip = StringField(u'IP', validators=[DataRequired(u"必填项"), Length(7, 15)])
    username = StringField(u'用户名', validators=[DataRequired(u"必填项"), Length(1, 20)])
    password = StringField(u'密码', validators=[DataRequired(u"必填项"), Length(6, 20)])
    notes = TextAreaField(u'备注', validators=[Length(max=200)])
    submit = SubmitField(u'提交')

