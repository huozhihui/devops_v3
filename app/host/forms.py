#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, \
    TextAreaField, DateField, IntegerField
from wtforms.validators import Required, DataRequired, Optional


# 定义表单类
class HostForm(FlaskForm):
    username = StringField(u'用户名', validators=[DataRequired(u"必填项")], default='root')
    password = StringField(u'密码', validators=[DataRequired(u"必填项")])
    ip = StringField(u'IP', validators=[DataRequired(u"必填项")])
    port = StringField(u'端口', validators=[DataRequired(u"必填项")], default=22)
    notes = TextAreaField(u'备注')
    submit = SubmitField(u'提交')
