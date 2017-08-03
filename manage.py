#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, time, threading
from flask import Flask, current_app, url_for
from app import create_app, db, system_data
from app.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
# from flask_socketio import SocketIO, emit

from app.websocket_method import *

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
# socketio = SocketIO(app)


# ===================================================
# 清除css,js缓存
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


# =====================================================
# websocket方法
# @socketio.on('connect_event')
# def connected_msg(msg):
#     method = msg.get('method')
#     data = msg.get('data')
#     # print method, data
#     if method:
#         eval(method)(data)

        # eval(msg)(msg)
        # emit('ws_problem_table', {'data': msg})
        # while True:
        #     msg = system_data.memory_used()
        #     emit('memory_used', {'data': msg})
        #     time.sleep(1)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


# @manager.command
# def run():
#     socketio.run(current_app,
#                  host='127.0.0.1',
#                  port=5000,
#                  use_reloader=False)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
