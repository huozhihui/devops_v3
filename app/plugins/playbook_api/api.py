#!/usr/bin/python
# -*- coding: utf-8 -*-
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor

# 自定义参数、结果
from options import options
from result import result_callback

loader = DataLoader()  # 用来加载解析yaml文件或JSON内容,并且支持vault的解密
variable_manager = VariableManager()  # 管理变量的类,包括主机,组,扩展等变量,之前版本是在 inventory 中的


def run_playbook(host_list, yml_list):
    inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=host_list)
    variable_manager.set_inventory(inventory)  # 根据 inventory 加载对应变量
    playbooks = yml_list  # 这里是一个列表, 因此可以运行多个playbook
    variable_manager.extra_vars = {}
    # variable_manager.extra_vars={"ansible_ssh_user":"root" , "ansible_ssh_pass":"root"}  # 增加外部变量
    pb = PlaybookExecutor(playbooks=playbooks, inventory=inventory, variable_manager=variable_manager, loader=loader,
                          options=options, passwords=None)
    pb._tqm._stdout_callback = result_callback
    result = pb.run()
    return result, result_callback


if __name__ == '__main__':
    host_list = "/tmp/20170720113901-62/hosts"
    yml_list = ['/Users/huozhihui/temp/ansible/nginx_install.yaml', '/Users/huozhihui/temp/ansible/ntp.yml']
    yml_list = ['/tmp/20170720113901-62/task.yml']
    code, result =run_playbook(host_list, yml_list)
    print code
    # print result
    print result.host_ok
    print result.host_failed
    print result.host_unreachable

