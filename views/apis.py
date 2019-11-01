# -*- coding: utf8 -*-
# @Author: SamSa
from django.shortcuts import render

from libs.http import render_json
from libs.view import BaseView


class Test(BaseView):
    def get(self, request):
        """
        测试
        """
        res = {'test': 'this is a test'}
        # return render_json(data=[])
        return render(request, 'show/base.html')
