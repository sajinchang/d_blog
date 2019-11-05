# -*- coding: utf-8 -*-
# @Author  : SamSa
# redis连接
from redis import Redis
from django.conf import settings

rds = Redis(**settings.REDIS)
