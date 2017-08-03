#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, \
    TextAreaField, DateField, IntegerField
from wtforms.validators import Required, DataRequired, Optional


# 定义表单类
class InventoryForm(FlaskForm):
    # type = StringField(u'设备类型', validators=[DataRequired("Please Enter your birthdate")])
    # type = StringField(u'设备类型', validators=[DataRequired(u"必填项")])
    type = StringField(u'设备类型')
    brand = StringField(u'设备品牌')
    asset_tag = StringField(u'资产标签')
    hostid = IntegerField(u'设备ID', default=0)
    name = StringField(u'设备名称')
    used = TextAreaField(u'用途或描述')
    os = StringField(u'操作系统')
    os_short = StringField(u'操作系统简写')
    os_digits = StringField(u'系统位数')
    os_full = TextAreaField(u'系统描述')
    mac_address = StringField(u'Mac地址')
    serial_no = StringField(u'序列号')

    host_networks = TextAreaField(u'主机网络')
    host_netmask = StringField(u'主机子网掩码')
    host_router = StringField(u'主机路由')
    oob_ip = StringField(u'外 IP 地址')
    oob_netmask = StringField(u'外子网掩码')
    oob_router = StringField(u'外路由器')

    date_hw_purchase = DateField(u'购买日期', validators=[Optional()])
    date_hw_install = DateField(u'安装日期', validators=[Optional()])
    date_hw_expiry = DateField(u'过保日期', validators=[Optional()])
    date_hw_decomm = DateField(u'退役日期', validators=[Optional()])
    cabinet = StringField(u'所在机柜')
    rack = StringField(u'所在机架')
    location = TextAreaField(u'详细位置')
    department = StringField(u'所属部门')
    contact = StringField(u'负责人')
    contact_tel = StringField(u'电话')
    contact_phone = StringField(u'手机')
    contact_email = StringField(u'Email')
    notes = TextAreaField(u'备注')

    # name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField(u'提交')
