#!/usr/bin/python
# -*- coding: utf-8 -*-
import tempfile


#
# class AnsibleError(Exception):
#     def __init__(self, value):
#         self.value = value
#
#     def __str__(self):
#         return repr(self.value)
#
#
# class AnsibleHost():
#     def __init__(self, **kwargs):
#         self.ip = '127.0.0.1'
#         self.ansible_connection = 'ssh'
#         self.ansible_ssh_user = kwargs.get('username', 'root')
#         self.ansible_ssh_pass = kwargs.get('password', None)
#         self.ansible_ssh_port = kwargs.get('port', 22)
#
#     def get_dict(self):
#         if not self.ansible_ssh_pass:
#             raise AnsibleError('ansible_ssh_pass is None')
#         return dict(ip=self.ip,
#                     ansible_connection=self.ansible_connection,
#                     ansible_ssh_user=self.ansible_ssh_user,
#                     ansible_ssh_pass=self.ansible_ssh_pass,
#                     ansible_ssh_port=self.ansible_ssh_port
#                     )


def create_hosts(host_dict):
    if not isinstance(host_dict, dict):
        return None

    temp = tempfile.NamedTemporaryFile()
    for ip, value in host_dict.items():
        if ip in ['127.0.0.1', 'localhost']:
            continue
        username = value.get('ansible_ssh_user', 'root')
        password = value.get('ansible_ssh_pass', '')
        port = value.get('ansible_ssh_port', 22)
        conn = value.get('ansible_connection', 'ssh')
        s = "{ip} ansible_ssh_user={username} ansible_ssh_pass={password} ansible_ssh_port={port} ansible_connection={conn}\n"
        line = s.format(ip=ip, username=username, password=password, port=port, conn=conn)
        temp.write(line)
    temp.seek(0)
    if temp.read() == '':
        temp.close()
        return None
    else:
        print "ansible host cache file: %s" % temp.name
        return temp


if __name__ == '__main__':
    hosts = {}
    d = dict(ansible_connection='ssh',
             ansible_ssh_user='root',
             ansible_ssh_pass='aaa',
             ansible_ssh_port=24)
    hosts['127.0.0.1'] = d
    d = dict(ansible_connection='ssh',
             ansible_ssh_user='root',
             ansible_ssh_pass='bbb',
             ansible_ssh_port=25)
    hosts['127.0.0.2'] = d

    host_file = create_hosts(hosts)
    print host_file.read()
    host_file.close()
