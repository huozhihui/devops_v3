#!/usr/bin/python
# -*- coding: utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from . import db
from . import login_manager
from datetime import datetime
from collections import OrderedDict


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __getitem__(self, item):
        return self.__dict__[item]


class CommonName(db.Model):
    __abstract__ = True
    name = db.Column(db.String(50))


class CommonNotes(db.Model):
    __abstract__ = True
    notes = db.Column(db.Text())


# 定义数据库模型
class Role(Base):
    __tablename__ = 'roles'
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, Base):
    __tablename__ = 'users'
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # 邮件确认字段
    confirmed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 登陆时,加载用户的回调函数
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # 发送邮件时生成token
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True


# 定义主机IP管理模型
class Host(Base):
    __tablename__ = 'hosts'
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    ip = db.Column(db.String(15), unique=True)
    port = db.Column(db.Integer, default=22)
    status = db.Column(db.Boolean, default=False)
    # 添加方式, manual手动, auto自动
    add_way = db.Column(db.String(10), default='manual')
    notes = db.Column(db.TEXT())
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventorys.id'))

    def __repr__(self):
        return '<Host %r>' % self.ip

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    def status_name(self):
        return ''

    def status_color(self):
        return ''


# 主机组和主机资产管理, 多对多
mid_host_group_inventorys = db.Table('mid_host_group_inventorys',
                                     db.Column('groupid', db.Integer, db.ForeignKey('host_groups.groupid')),
                                     db.Column('hostid', db.Integer, db.ForeignKey('inventorys.hostid'))
                                     )


# 主机资产信息
class Inventory(Base):
    __tablename__ = 'inventorys'
    hostid = db.Column(db.Integer, default=0)
    type = db.Column(db.String(50))
    brand = db.Column(db.String(100))
    asset_tag = db.Column(db.String(50))
    name = db.Column(db.String(50))
    used = db.Column(db.TEXT())
    os = db.Column(db.String(100))
    os_short = db.Column(db.String(50))
    os_digits = db.Column(db.String(50))
    os_full = db.Column(db.TEXT())
    mac_address = db.Column(db.String(50))
    serial_no = db.Column(db.String(50))
    # 主机网络
    host_networks = db.Column(db.TEXT())
    host_netmask = db.Column(db.String(50))
    host_router = db.Column(db.String(50))
    oob_ip = db.Column(db.String(50))
    oob_netmask = db.Column(db.String(50))
    oob_router = db.Column(db.String(50))

    # date_hw_purchase = db.Column(db.DATE())
    # date_hw_install = db.Column(db.DATE())
    # date_hw_expiry = db.Column(db.DATE())
    # date_hw_decomm = db.Column(db.DATE())
    date_hw_purchase = db.Column(db.String(50))
    date_hw_install = db.Column(db.String(50))
    date_hw_expiry = db.Column(db.String(50))
    date_hw_decomm = db.Column(db.String(50))

    cabinet = db.Column(db.String(100))
    rack = db.Column(db.String(100))
    location = db.Column(db.TEXT())
    department = db.Column(db.String(100))
    contact = db.Column(db.String(50))
    contact_tel = db.Column(db.String(50))
    contact_phone = db.Column(db.String(50))
    contact_email = db.Column(db.String(50))
    notes = db.Column(db.TEXT())
    hosts = db.relationship('Host', backref='inventory', lazy='dynamic')
    inventory_updates = db.relationship('InventoryUpdate', backref='inventory', lazy='dynamic')


    def __repr__(self):
        return '<Inventory %r>' % self.name

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    # def match_zabbix(self):
    #     common = ["type", "asset_tag", "name", "os", "os_short", "os_digits", "os_full",
    #               "mac_address", "serial_no", "host_networks", "host_netmask", "host_router",
    #               "oob_ip", "oob_netmask", "oob_router", "date_hw_purchase", "date_hw_install",
    #               "date_hw_expiry", "date_hw_decomm", "location", "notes"]
    #
    #     without = ["brand", "used", "cabinet", "rack", "department", "contact", "contact_tel",
    #                "contact_phone", "contact_email"]
    #
    #     tmp_dict = OrderedDict()
    #     for key in common:
    #         tmp_dict[key] = key
    #     tmp_dict.update(dict(os_digits="software", mac_address="macaddress_a", serial_no="serialno_a"))
    #     return tmp_dict

    # 获取机器所有IP
    def ips(self):
        return ','.join([h.ip for h in self.hosts])

    # 获取机器状态名称
    def status_name(self):
        return ''

    # 获取机器状态颜色
    def status_color(self):
        return ''


class InventoryUpdate(Base):
    __tablename__ = 'inventory_updates'
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventorys.id'))
    content = db.Column(db.TEXT())

    def __repr__(self):
        return '<InventoryUpdate %r>' % self.id


class HostGroup(Base):
    __tablename__ = 'host_groups'
    name = db.Column(db.String(50), unique=True)
    groupid = db.Column(db.Integer, default=0)
    notes = db.Column(db.TEXT())

    hosts = db.relationship('Inventory', secondary=mid_host_group_inventorys,
                            backref=db.backref('host_groups', lazy='dynamic'))


    def __repr__(self):
        return '<HostGroup %r>' % self.name


# 定义作业模型
class Homework(Base):
    __tablename__ = 'homeworks'
    # id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    notes = db.Column(db.Text())
    tasks = db.relationship('Task', backref='homework', lazy='dynamic')

    def __repr__(self):
        return '<Homework %r>' % self.name


# 定义组件模型
class Component(Base):
    __tablename__ = 'components'
    # id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    type = db.Column(db.String(20))
    version = db.Column(db.String(50))
    os = db.Column(db.String(50))
    content = db.Column(db.Text())
    notes = db.Column(db.Text())
    upload_files = db.relationship('UploadFile', backref='component', lazy='dynamic')
    variables = db.relationship('Variable', backref='component', lazy='dynamic')

    def __repr__(self):
        return '<Component %r>' % self.name


# 定义上传文件模型
class UploadFile(Base):
    __tablename__ = 'upload_files'
    # id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    path = db.Column(db.String(100))
    type = db.Column(db.String(50))
    notes = db.Column(db.Text())
    component_id = db.Column(db.Integer, db.ForeignKey('components.id'))

    def __repr__(self):
        return '<UploadFile %r>' % self.name


# 定义上传文件模型
class Variable(Base):
    __tablename__ = 'variables'
    # id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    value = db.Column(db.String(100))
    type = db.Column(db.String(50))
    notes = db.Column(db.Text())
    component_id = db.Column(db.Integer, db.ForeignKey('components.id'))

    def __repr__(self):
        return '<Variable %r>' % self.name


mid_task_hosts = db.Table('mid_task_hosts',
                          db.Column('task_id', db.Integer, db.ForeignKey('tasks.id')),
                          db.Column('host_id', db.Integer, db.ForeignKey('hosts.id'))
                          )

mid_task_components = db.Table('mid_task_components',
                               db.Column('task_id', db.Integer, db.ForeignKey('tasks.id')),
                               db.Column('component_id', db.Integer, db.ForeignKey('components.id'))
                               )

mid_task_variables = db.Table('mid_task_variables',
                              db.Column('task_id', db.Integer, db.ForeignKey('tasks.id')),
                              db.Column('variable_id', db.Integer, db.ForeignKey('variables.id')),
                              db.Column('value', db.String(100))
                              )


# 定义作业模型
class Task(Base):
    __tablename__ = 'tasks'
    # id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    status = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text())
    homework_id = db.Column(db.Integer, db.ForeignKey('homeworks.id'), nullable=False)
    task_results = db.relationship('TaskResult', backref='task', lazy='dynamic')
    components = db.relationship('Component', secondary=mid_task_components,
                                 backref=db.backref('tasks', lazy='dynamic'))
    hosts = db.relationship('Host', secondary=mid_task_hosts,
                            backref=db.backref('tasks', lazy='dynamic'))
    # variables = db.relationship('Variable', secondary=mid_task_variables,
    #                             backref=db.backref('tasks', lazy='dynamic'))

    variables = db.Column(db.Text())

    # 是否配置主机
    def is_configured(self):
        if len(self.hosts) > 0:
            return True
        else:
            return False

    # def status_name(self):
    #     if len(self.hosts) == 0:
    #         return

    # 获取任务的所有组件
    def get_components(self):
        return ','.join([c.name for c in self.components])

    # 获取任务的所有主机
    def get_ips(self):
        return ','.join([h.ip for h in self.hosts])

    # 获取任务的所有变量
    # def get_variables(self):
    #     return ','.join([v.name for v in self.variables])

    def __repr__(self):
        return '<Task %r>' % self.name


class TaskResult(Base):
    __tablename__ = 'task_results'
    # id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))

    def __repr__(self):
        return '<TaskResult %r>' % self.task_id


# 脚本管理
class ScriptManage(CommonName, Base):
    __tablename__ = 'script_manages'
    type = db.Column(db.String(50))
    content = db.Column(db.Text())
    notes = db.Column(db.Text())
    variables = db.relationship('ScriptVariable', backref='script_manage', lazy='dynamic')

    def type_name(self):
        d = dict(sh='shell', py="python", yml='yaml')
        return d.get(self.type, '')

    def __repr__(self):
        return '<ScriptManage %r>' % self.name


# 定义脚本变量模型
class ScriptVariable(CommonNotes, CommonName, Base):
    __tablename__ = 'script_variables'
    script_manage_id = db.Column(db.Integer, db.ForeignKey('script_manages.id'))

    def __repr__(self):
        return '<ScriptVariable %r>' % self.name


# 定义Zabbix模型
class Zabbix(Base):
    __tablename__ = 'zabbixs'
    # id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15), unique=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    is_used = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text())


# 定义平台管理模型
class Cmp(Base):
    __tablename__ = 'cmps'
    name = db.Column(db.String(30), unique=True)
    groupid = db.Column(db.Integer)
    hostid = db.Column(db.Integer)
    notes = db.Column(db.TEXT())
    cmp_items = db.relationship('CmpItem', backref='cmp', lazy='dynamic')


    def __repr__(self):
        return '<Cmp %r>' % self.name


# 定义平台管理的展示项目模块
class CmpItem(Base):
    __tablename__ = 'cmp_items'
    name = db.Column(db.String(30), unique=True)
    applicationid = db.Column(db.Integer)
    itemid = db.Column(db.Integer)
    value = db.Column(db.String(50))
    notes = db.Column(db.TEXT())
    cmp_id = db.Column(db.Integer, db.ForeignKey('cmps.id'))

    def __repr__(self):
        return '<CmpItem %r>' % self.name
