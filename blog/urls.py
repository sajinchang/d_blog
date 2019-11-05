# -*- coding: utf-8 -*-
# @Author  : SamSa
from django.conf.urls import url

from blog import views

urlpatterns = [
    url(r'^$', views.BlogView.as_view(), name='blog_list'),
    url(r'^(?P<pk>\d+)$', views.BlogShowView.as_view(), name='blog_show'),
    url(r'^tag/cache$', views.tag_cache, name='tag_cache'),
    url(r'^top/article$', views.top_article, name='top_article'),

    url(r'(?P<tag_category>\w*)/(?P<pk>\d+)', views.CategoryTagView.as_view(), name='category_tag'),
]