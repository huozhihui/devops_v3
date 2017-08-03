#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField, \
#     TextAreaField, DateField, IntegerField
from wtforms import *
from wtforms.validators import Required, DataRequired, Optional, Length


# 定义表单类
class ScriptForm(FlaskForm):
    # type = StringField(u'设备类型', validators=[DataRequired("Please Enter your birthdate")])
    name = StringField(u'脚本名称', validators=[DataRequired(u"必填项"), Length(1, 15)])
    type = SelectField(u'脚本类型',
                       choices=[('sh', 'Shell'), ('py', 'Python'), ('yml', 'Yaml')],
                       )
    # type = RadioField(u'脚本类型',
    #     [DataRequired(u"必填项")],
    #     choices=[('sh', 'Shell'), ('py', 'Python'), ('yml', 'Yaml')], default='Shell'
    # )
    content = TextAreaField(u'脚本内容', validators=[DataRequired(u"必填项")])
    notes = TextAreaField(u'备注', validators=[Length(max=200)])
    submit = SubmitField(u'提交')
