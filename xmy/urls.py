# -*- coding: utf-8 -*-
# @Author  : SamSa

from django.conf.urls import url

from .views import GalleryView
from .views import GalleryShowView


urlpatterns = [
    url(r'^$', GalleryView.as_view(), name='gallery'),
    url(r'^(?P<pk>\d+)$', GalleryShowView.as_view(), name='gallery_show')
]