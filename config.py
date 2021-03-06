#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from datetime import timedelta
from celery.schedules import crontab

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = '996748270@qq.com'
    # FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    # MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # 定时任务
    CELERY_BROKER_URL = 'redis://localhost:6379',
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    # CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERYBEAT_SCHEDULE = {
        'import_zabbix_data': {
            'task': 'import_zabbix_data',
            'schedule': timedelta(minutes=3)
            # 'schedule': 5.0
        },
        'import_item_value_data': {
            'task': 'import_item_value_data',
            'schedule': timedelta(minutes=1)
        }
    }

    # app.config['CELERYBEAT_SCHEDULE'] = {
    #     'play-every-morning': {
    #         'task': 'tasks.play_task',
    #         'schedule': crontab(hour=9, minute=0)
    #     },
    #     'pause-later': {
    #         'task': 'tasks.pause_task',
    #         'schedule': crontab(hour=9, minute=10)
    #     }
    # }

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
