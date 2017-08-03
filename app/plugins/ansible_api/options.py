#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import namedtuple

# 初始化需要的对象
Options = namedtuple('Options',
                     ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check'])

# # 初始化需要的对象
options = Options(connection='local',
                  module_path=None,
                  forks=100,
                  become=None,
                  become_method=None,
                  become_user=None,
                  check=False
                  )
