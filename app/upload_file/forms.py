#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Length


# 定义表单类
class ComponentForm(FlaskForm):
    name = StringField(u'名称', validators=[DataRequired(u"必填项"), Length(1, 20)], description=u"名称")
    type = SelectField(u'类型',
                       choices=[('install', u'安装'), ('upgrade', u'升级'),
                                ('optimize', u'优化'), ('uninstall', u'卸载')
                                ],
                       validators=[DataRequired(u"必填项")]
                       )
    version = StringField(u'版本', validators=[DataRequired(u"必填项"), Length(1, 20)])
    os = StringField(u'适用于(系统)', validators=[DataRequired(u"必填项"), Length(1, 20)])
    content = TextAreaField(u'脚本', validators=[DataRequired(u"必填项")])
    files = FileField(u'安装包/脚本上传')
    templates = FileField(u'配置/模版上传')
    notes = TextAreaField(u'备注', validators=[Length(max=200)])
    # submit = SubmitField(u'提交')
