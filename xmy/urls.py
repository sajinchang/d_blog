# -*- coding: utf-8 -*-
# @Author  : SamSa

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.GalleryView.as_view(), name='gallery'),
    url(r'^(?P<pk>\d+)$', views.GalleryShowView.as_view(), name='gallery_show'),
    url(r'^top$', views.GalleryTopView.as_view(), name='gallery_top'),
]