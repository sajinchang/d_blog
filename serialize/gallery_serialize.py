# -*- coding: utf-8 -*-
# @Author  : SamSa
from rest_framework import serializers

from xmy import models


class AlbumSerialize(serializers.ModelSerializer):
    album_create_at = serializers.DateTimeField('%Y-%m-%d %H:%M:%S')
    album_update_at = serializers.DateTimeField('%Y-%m-%d %H:%M:%S')

    class Meta:
        model = models.AlbumModel
        fields = '__all__'


class GallerySerialize(serializers.ModelSerializer):
    gallery_create_at = serializers.DateTimeField('%Y-%m-%d')
    gallery_update_at = serializers.DateTimeField('%Y-%m-%d %H:%M:%S')
    like_num = serializers.CharField(source='gallery_like.click_num')
    # 外键反向查询,序列化   必须指定外键 relate_name 字段和该字段一致, 否则找不到虚拟关系或者报错
    # gallery = AlbumSerialize(many=True, read_only=True, )
    gallery_count = serializers.SerializerMethodField()
    albums = serializers.SerializerMethodField()

    def get_albums(self, obj):
        return AlbumSerialize(instance=obj.albums, many=True).data

    def get_gallery_count(self, obj):
        """
        外键反向查询
        如果外键设置relate_name属性,则使用 obj.relate_name值.all()
        如果没有设置该属性, 使用obj.外键所在model名字_set.all()
        :param obj:
        :return:
        """
        return obj.gallery.filter(album_deleted=False).count()

    gallery_comment_short = serializers.SerializerMethodField()

    def get_gallery_comment_short(self, obj):
        """
        返回列表页少量简介
        :param obj:
        :return:
        """
        return obj.gallery_comment[:30]

    class Meta:
        model = models.GalleryModel
        fields = '__all__'
        depth = 2
