#!/usr/bin/python
# -*- coding: utf-8 -*-
from app import create_app
# 必须导入celery
from app import celery
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    app.run()
