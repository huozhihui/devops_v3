#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit
import psutil as ps
import time

app = Flask(__name__, template_folder='./')
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect_event')
def connected_msg(msg):
    while True:
        send_memory_used()


# 实时发送已用内存
def send_memory_used():
    mem = ps.virtual_memory()
    total = mem.total / 1024 ** 3
    used = int(round(total * mem.percent / 100))
    emit('memory_used', {'data': used})
    time.sleep(1)


# @socketio.on('disconnect')
# def disconnect():
#     print('Client disconnected')


# @socketio.on_error_default
# def default_error_handler(e):
#     print('Error msg:')
#     print(request.event["message"]) # "my error event"
#     print(request.event["args"])    # (data,)

if __name__ == '__main__':
    # socketio.run(app, host='0.0.0.0')
    socketio.run(app, host='127.0.0.1', port='5001')
