#!/usr/bin/python
# -*- coding: utf-8 -*-
# from flask import Flask
from app import create_app, socketio
import os
from flask import url_for


# def create_app():
#     # 这个工厂方法可以从你的原有的 `__init__.py` 或者其它地方引入。
#     app = Flask(__name__)
#     return app


application = create_app(os.getenv('FLASK_CONFIG') or 'default')

# 清除css,js缓存
@application.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(application.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == '__main__':
    application.run()
    # 如果打开socketio时, 调用ansible接口失败
    # socketio.run(application)
