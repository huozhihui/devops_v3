#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy, Model
# from sqlalchemy import Column, DateTime
from config import config
from flask_login import LoginManager
# from flask_navigation import Navigation
from flask_socketio import SocketIO, emit
from flask_celery import Celery

bootstrap = Bootstrap()
# nav = Navigation()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
socketio = SocketIO()
celery = Celery()

# 设置登陆
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


# 设置上传路径
# UPLOAD_FOLDER = '/path/to/the/uploads'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    celery.init_app(app)

    # 定时任务
    from .celery_manage import celery_manage as celery_manage_blueprint
    app.register_blueprint(celery_manage_blueprint, url_prefix='/celery_manage')

    # zabbix_api蓝本
    from .zabbix_api import zabbix_api as zabbix_api_blueprint
    app.register_blueprint(zabbix_api_blueprint, url_prefix='/zabbix_api/v1')

    # from .zabbix import zabbix as zabbix_blueprint
    # app.register_blueprint(zabbix_blueprint, url_prefix='/zabbix_api/v1')

    from .zabbix import zabbix as zabbix_blueprint
    app.register_blueprint(zabbix_blueprint, url_prefix='/zabbix')

    # 身份验证蓝本
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # 首页-蓝本
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(main_blueprint, url_prefix='/main')


    # 主机组蓝本
    from .host_group import host_group as host_group_blueprint
    app.register_blueprint(host_group_blueprint, url_prefix='/host_group')

    # 主机蓝本
    from .host import host as host_blueprint
    app.register_blueprint(host_blueprint, url_prefix='/host')

    # 资产管理-蓝本
    from .inventory import inventory as inventory_blueprint
    app.register_blueprint(inventory_blueprint, url_prefix='/inventory')

    # 资产变更管理-蓝本
    from .inventory_update import inventory_update as inventory_update_blueprint
    app.register_blueprint(inventory_update_blueprint, url_prefix='/inventory_update')

    # 监控报警-蓝本
    from .problem import problem as problem_blueprint
    app.register_blueprint(problem_blueprint, url_prefix='/problem')

    # 自动化运维, 脚本管理-蓝本
    from .script_manage import script_manage as script_manage_blueprint
    app.register_blueprint(script_manage_blueprint, url_prefix='/script_manage')

    # 自动化运维, 作业管理-蓝本
    from .homework import homework as homework_blueprint
    app.register_blueprint(homework_blueprint, url_prefix='/homework')

    # 自动化运维, 组件管理-蓝本
    from .component import component as component_blueprint
    app.register_blueprint(component_blueprint, url_prefix='/component')

    # 自动化运维, 变量管理-蓝本
    from .variable import variable as variable_blueprint
    app.register_blueprint(variable_blueprint, url_prefix='/variable')

    # 自动化运维, 文件管理-蓝本
    from .upload_file import upload_file as upload_file_blueprint
    app.register_blueprint(upload_file_blueprint, url_prefix='/upload_file')

    # 任务编排-蓝本
    from .task import task as task_blueprint
    app.register_blueprint(task_blueprint, url_prefix='/task')

    # 云平台管理-蓝本
    from .cmp import cmp as cmp_blueprint
    app.register_blueprint(cmp_blueprint, url_prefix='/cmp')

    # 云平台监控项管理-蓝本
    from .cmp_item import cmp_item as cmp_item_blueprint
    app.register_blueprint(cmp_item_blueprint, url_prefix='/cmp_item')

    # 附加路由和自定义的错误页面
    return app

