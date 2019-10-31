# -*- coding=utf8 -*-
# @Author: SamSa

from django.conf import settings
from django.http import JsonResponse


def render_json(code=0, count=0, data=None, msg=''):
    """
    :param count:   type: int     返回数据总量
    :param code:    type: int     状态吗
    :param data:    type: list    数据
    :param msg:     type: str     信息
    """
    result = {
        'code': code,
        'msg': msg,
        'count': count,
        'data': data
    }
    return JsonResponse(result, safe=True)
