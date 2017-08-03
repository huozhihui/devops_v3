#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.plugins.callback import CallbackBase
import json


class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    def __init__(self, *args, **kwargs):
        super(ResultCallback, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host.get_name()
        task_name = unicode(result._task.name)
        print task_name
        print host
        print result._result
        self.host_ok[host] = result._result

    def v2_runner_on_unreachable(self, result, **kwargs):
        host = result._host.get_name()
        task_name = unicode(result._task.name)
        print task_name
        print host
        print result._result
        self.host_unreachable[host] = result._result
        # print json.dumps({host: result._result}, indent=4)

    def v2_runner_on_failed(self, result, **kwargs):
        host = result._host.get_name()
        task_name = unicode(result._task.name)
        print "44444444444444"
        print task_name
        print host
        print result._result
        self.host_failed[host] = result._result
        print "5555555555555555"
        print self.host_failed


result_callback = ResultCallback()
