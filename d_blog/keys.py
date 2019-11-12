# -*- coding: utf-8 -*-
# @Author  : SamSa
from django.conf import settings

# redis key  排行榜
RANK_ARTICLE = '%s%s' % (settings.SECRET_KEY, 'rank_article')

# 登陆url
LOGIN_URL = '/admin/login'
SERVER_ERROR = 500
FORM_ERROR = 501
COMMENT_ERROR = 502
