#!/usr/bin/python
# -*- coding: utf-8 -*-
# 获取系统数据
import psutil as ps

# 内存
memory = ps.virtual_memory()
memory_total = memory.total / 1024 ** 3
memory_percent = memory.percent
memory_used = int(round(memory_total * memory_percent / 100))

# 磁盘
disk = ps.disk_usage('/')
disk_total = disk.total / 1024 ** 3
disk_percent = disk.percent
disk_used = int(round(disk_total * disk_percent / 100))

# CPU
cpu_percent = ps.cpu_percent(0) # 使用率
cpu_count = ps.cpu_count(logical=False) # 核数



'''
# 内存总计
def memory_total():
    total = mem.total / 1024 ** 3
    return total


# 内存百分比
def memory_percent():
    percent = mem.percent
    return percent


# 已用内存
def memory_used():
    used = int(round(memory_total() * memory_percent() / 100))
    return used

# 内存总计
def memory_total():
    total = mem.total / 1024 ** 3
    return total


# 内存百分比
def memory_percent():
    percent = mem.percent
    return percent


# 已用内存
def memory_used():
    used = int(round(memory_total() * memory_percent() / 100))
    return used
'''