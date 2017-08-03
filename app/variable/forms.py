#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Length


# 定义表单类
class VariableForm(FlaskForm):
    name = StringField(u'名称', validators=[DataRequired(u"必填项"), Length(1, 20)], description=u"名称")
    # type = SelectField(u'类型',
    #                    choices=[('install', u'安装'), ('upgrade', u'升级'),
    #                             ('optimize', u'优化'), ('uninstall', u'卸载')
    #                             ],
    #                    validators=[DataRequired(u"必填项")]
    #                    )
    value = StringField(u'默认值', validators=[Length(1, 20)])
    type =  RadioField(u'类型', choices=[('default',u'默认'),('dynamic',u'动态')])
    notes = TextAreaField(u'备注', validators=[Length(max=200)])
    # submit = SubmitField(u'提交')
