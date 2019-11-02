# -*- coding: utf-8 -*-
# @Author  : SamSa
from rest_framework import serializers

from xmy import models as Gallery


class AlbumSerialize(serializers.ModelSerializer):
    album_create_at = serializers.DateTimeField('%Y-%m-%d %H:%M:%S')
    album_update_at = serializers.DateTimeField('%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Gallery.AlbumModel
        fields = '__all__'


class GallerySerialize(serializers.ModelSerializer):
    gallery_create_at = serializers.DateTimeField('%Y-%m-%d %H:%M:%S')
    gallery_update_at = serializers.DateTimeField('%Y-%m-%d %H:%M:%S')

    # 外键反向查询,序列化   必须指定外键 relate_name 字段和该字段一致, 否则找不到虚拟关系或者报错
    gallery = AlbumSerialize(many=True, read_only=True)

    class Meta:
        model = Gallery.GalleryModel
        fields = '__all__'
