# -*- coding: utf8 -*-
# @Author: SamSa

LOG_DIR = '/app/d_blog/logs'

MEDIA_ROOT = '/app/d_blog/media/upload'

# [MYSQL]
DB = {
    'USER': 'root',
    'PORT': 3306,
    'NAME': 'blog',
    'PASSWORD': '123456',
    'HOST': '127.0.0.1'
}

# [REDIS]
REDIS = {
    'HOST': '127.0.0.1',
    'DB': '1',
    'PORT': 6379
}
