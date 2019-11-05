# -*- coding: utf8 -*-
# @Author: SamSa
from django.shortcuts import render

from blog.models import ArticleModel
from libs.http import render_json
from libs.utils import query_page
from libs.view import BaseView
from serialize.blog_serialize import ArticleSerialize


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
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        queryset = ArticleModel.objects.filter(article_deleted=False)
        result = query_page(pre_page=limit, pages=9, current_page=page,
                            queryset=queryset, serialize=ArticleSerialize)
        # return render_json(data=result)
        return render(request, 'show/index.html', context=result)
