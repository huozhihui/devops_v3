#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_socketio import emit
import time
import json
from collections import OrderedDict
import zabbix


# 更新报警列表数据
def ws_problem_update_table(msg):
    while True:
        problems = zabbix_api.trigger.problems()
        data = []
        priority_color = []
        for pb in problems:
            data.append([
                pb.host_name,
                # pb.priority_color,
                pb.priority_name,
                pb.status_name,
                pb.last_change,
                pb.up_to_now(),
                pb.description
            ])
            priority_color.append(pb.priority_color)
        emit('ws_problem_update_table', {'data': data})
        emit('ws_problem_update_priority_color', {'data': priority_color})
        time.sleep(5)
