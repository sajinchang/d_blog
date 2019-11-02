# -*- coding: utf-8 -*-
# @Author  : SamSa
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render


@csrf_exempt
def page_not_found(request, *args, **kwargs):
    """
    404 error
    :param request:
    :return:
    """
    return render(request, 'error/error.html', context={'code': 404, 'msg': '页面去火星了!'})


@csrf_exempt
def server_error(request, *args, **kwargs):
    """
    server error 500
    :param request:
    :return:
    """
    return render(request, 'error/error.html', context={'code': 500, 'msg': '啊,程序员又写bug了!'})
