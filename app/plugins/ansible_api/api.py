#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import datetime
import random
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
# 自定义hosts文件、参数及结果
from hosts import create_hosts
from options import options
from result import ResultCallback

loader = DataLoader()  # 用来加载解析yaml文件或JSON内容,并且支持vault的解密
variable_manager = VariableManager()  # 管理变量的类,包括主机,组,扩展等变量,之前版本是在 inventory 中的



def run(hosts, module_name, params, extra_vars={}):
    host_file = create_hosts(hosts)
    if host_file:
        inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=host_file.name)
    else:
        inventory = Inventory(loader=loader, variable_manager=variable_manager)
    variable_manager.set_inventory(inventory)  # 根据 inventory 加载对应变量
    variable_manager.extra_vars = extra_vars  # 增加外部变量
    # 构建pb, 这里很有意思, 新版本运行ad-hoc或playbook都需要构建这样的pb, 只是最后调用play的类不一样
    # :param name: 任务名,类似playbook中tasks中的name
    # :param hosts: playbook中的hosts
    # :param tasks: playbook中的tasks, 其实这就是playbook的语法, 因为tasks的值是个列表,因此可以写入多个task
    play_source = {"name": "Ansible Ad-Hoc",
                   "hosts": hosts.keys(),
                   "gather_facts": "no",
                   "tasks": [
                       # {"action":{"module":"shell","args":"w"}}
                       {"action": {"module": module_name, "args": params}}
                   ]
                   }
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
    result_callback = ResultCallback()  # 自定义结果
    tqm = None
    try:
        tqm = TaskQueueManager(
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            options=options,
            passwords=None,
            stdout_callback=result_callback,
            run_tree=False,
        )

        code = tqm.run(play)
        return code, result_callback
    finally:
        if tqm is not None:
            tqm.cleanup()
        if host_file is not None:
            host_file.close()


if __name__ == '__main__':
    # ext_vars = {"ansible_ssh_user":"root" , "ansible_ssh_pass":"root"}
    # params = {"name": "user01", "state": "absent", "remove": "yes"}
    hosts = {
        "127.0.0.1": {"ansible_connection": "ssh", "ansible_ssh_user": 'root', "ansible_ssh_pass": 'aaaa',
                      'ansible_ssh_port': 22},
        "10.43.1.30": {"ansible_connection": "ssh", "ansible_ssh_user": 'root', "ansible_ssh_pass": 'bbbb',
                       'ansible_ssh_port': 22},
    }
    params = "/Users/huozhihui/temp/ansible/cpu.sh"
    code, response = run(hosts, 'script', params)
    print code, response.result
