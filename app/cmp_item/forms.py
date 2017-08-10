#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, \
    TextAreaField, DateField, IntegerField, HiddenField
from wtforms.validators import Required, DataRequired, Optional


# 定义表单类
class CmpItemForm(FlaskForm):
    name = StringField(u'名称', validators=[DataRequired(u"必填项")])
    # value_type = HiddenField(u'数值类型')
    notes = TextAreaField(u'备注')
    # submit = SubmitField(u'提交')
