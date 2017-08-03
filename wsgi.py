#!/usr/bin/python
# -*- coding: utf-8 -*-
# from flask import Flask
from app import create_app
import os


# def create_app():
#     # 这个工厂方法可以从你的原有的 `__init__.py` 或者其它地方引入。
#     app = Flask(__name__)
#     return app


application = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    application.run()
