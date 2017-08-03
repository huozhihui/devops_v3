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
# 自定义参数、结果
from options import options
from result import result_callback

loader = DataLoader()                     # 用来加载解析yaml文件或JSON内容,并且支持vault的解密
variable_manager = VariableManager()      # 管理变量的类,包括主机,组,扩展等变量,之前版本是在 inventory 中的



def run(hosts, module_name, params, extra_vars={}):
    inventory = Inventory(loader=loader, variable_manager=variable_manager)
    variable_manager.set_inventory(inventory)  # 根据 inventory 加载对应变量
    variable_manager.extra_vars= extra_vars  # 增加外部变量
    # 构建pb, 这里很有意思, 新版本运行ad-hoc或playbook都需要构建这样的pb, 只是最后调用play的类不一样
    # :param name: 任务名,类似playbook中tasks中的name
    # :param hosts: playbook中的hosts
    # :param tasks: playbook中的tasks, 其实这就是playbook的语法, 因为tasks的值是个列表,因此可以写入多个task
    play_source = {"name": "Ansible Ad-Hoc",
                   "hosts": hosts,
                   "gather_facts": "no",
                   "tasks":[
                       # {"action":{"module":"shell","args":"w"}}
                       {"action":{"module":module_name,"args": params}}
                   ]
                   }
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
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



if __name__ == '__main__':
    #ext_vars = {"ansible_ssh_user":"root" , "ansible_ssh_pass":"root"}
    # params = {"name": "user01", "state": "absent", "remove": "yes"}
    #params = {"name": "user05", "password": "abc"}
    #dt = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    #rand = random.randint(10, 99)
    #tid = "{dt}-{rand}".format(dt=dt, rand=rand)
    params = "/Users/huozhihui/temp/ansible/cpu.sh aa"
    run('192.168.1.104', 'script', params)

