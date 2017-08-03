#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, \
    TextAreaField, DateField, IntegerField
from wtforms.validators import Required, DataRequired, Optional


# 定义表单类
class CmpItemForm(FlaskForm):
    name = StringField(u'组名', validators=[DataRequired(u"必填项")])
    notes = TextAreaField(u'备注')
    submit = SubmitField(u'提交')
