#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import namedtuple

# 初始化需要的对象
Options = namedtuple('Options',
                     ['connection',
                      'remote_user',
                      'ask_sudo_pass',
                      'verbosity',
                      'ack_pass',
                      'module_path',
                      'forks',
                      'become',
                      'become_method',
                      'become_user',
                      'check',
                      'listhosts',
                      'listtasks',
                      'listtags',
                      'syntax',
                      'sudo_user',
                      'sudo'])
# # 初始化需要的对象
options = Options(connection='smart',
                  remote_user='root',
                  ack_pass=None,
                  sudo_user='root',
                  forks=5,
                  sudo='yes',
                  ask_sudo_pass=False,
                  verbosity=5,
                  module_path=None,
                  become=True,
                  become_method='sudo',
                  become_user='root',
                  check=None,
                  listhosts=None,
                  listtasks=None,
                  listtags=None,
                  syntax=None)
