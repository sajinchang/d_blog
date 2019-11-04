# -*- coding: utf-8 -*-
# @Author  : SamSa
from django.conf.urls import url

from views import apis
from blog.views import BlogShowView
from blog.views import tag_cache

urlpatterns = [
    url(r'^$', apis.Index.as_view(), name='index'),
    url(r'^(?P<pk>\d+)$', BlogShowView.as_view(), name='blog_show'),
    url(r'^tag/cache$', tag_cache, name='tag_cache'),
]