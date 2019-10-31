# -*- coding: utf8 -*-
# @Author: SamSa


import os
# import sys
# import django

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elevator_temp.settings')
# django.setup()
from multiprocessing import cpu_count

import conf as my_config

# sys.path.insert(0, '../')
bind = ["127.0.0.1:8001"]  # 线上环境不会开启在公网 IP 下，一般使用内网 IP
daemon = True  # 是否开启守护进程模式
# daemon = False  # 是否开启守护进程模式
pidfile = os.path.join(my_config.LOG_DIR, 'gunicorn.pid')

# chdir = "/home/sam/work/qyhome"
workers = cpu_count()  # 工作进程数量
worker_class = "gevent"  # 指定一个异步处理的库
worker_connections = 65535
# gevent_monkey_patch = True #gevent协程补丁
keepalive = 60  # 服务器保持连接的时间，能够避免频繁的三次握手过程
timeout = 30
graceful_timeout = 10
forwarded_allow_ips = '*'

# 日志处理
capture_output = True
loglevel = 'debug'
errorlog = os.path.join(my_config.LOG_DIR, 'error.log')
# proc_name = 'project_name'