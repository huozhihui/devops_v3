#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Length


# 定义表单类
class TaskForm(FlaskForm):
    # name = StringField(u'名称', validators=[DataRequired(u"必填项"), Length(1, 20)])
    notes = TextAreaField(u'备注', validators=[Length(max=200)])
    submit = SubmitField(u'保存')

