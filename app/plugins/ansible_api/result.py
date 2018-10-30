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
        self.result = {}

    def v2_runner_on_ok(self, result, **kwargs):
        self.runner('ok', result)

    def v2_runner_on_unreachable(self, result, **kwargs):
        self.runner('unreachable', result)

    def v2_runner_on_failed(self, result, **kwargs):
        self.runner('failed', result)

    def v2_runner_on_skipped(self, result, **kwargs):
        self.runner('skipped', result)

    def runner(self, status, result):
        host = result._host.get_name()
        if status == 'failed':
            output = result._result.get('stderr', '')
        elif status == 'unreachable':
            output = result._result.get('msg', '')
        else:
            if result._result.get('stdout', '') == '':
                status = 'failed'
                output = result._result.get('stderr', '')
            else:
                status = 'changed'
                output = result._result.get('stdout', '')

        output = output.strip('\r\n')

        print "*******************************************************************"
        print u"执行主机: {ip}".format(ip=host)
        print u"任务状态: {status}".format(status=status)
        print u"任务结果: {output}".format(output=output)
        print u"任务总结果: {result}".format(result=result._result)
        self.result[host] = dict(status=status, output=output)
