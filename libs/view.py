# -*- coding: utf8 -*-
# @Author: SamSa

from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView


class BaseView(APIView):
    """
    rest_framework view, 重写dispatch方法, 进行csrf验证
    """
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)