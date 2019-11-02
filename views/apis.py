# -*- coding: utf8 -*-
# @Author: SamSa
from django.shortcuts import render

from libs.view import BaseView


class Test(BaseView):
    def get(self, request):
        """
        测试
        """
        res = {'test': 'this is a test'}
        return render(request, 'show/base.html')


class Index(BaseView):
    """首页"""
    def get(self, request):
        """

        :param request:
        :return:
        """
        return render(request, 'show/index.html')
