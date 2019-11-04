# -*- coding: utf-8 -*-
# @Author  : SamSa

from rest_framework import serializers
from blog import models
from libs.blog_tags import markdown_detail


class CategorySerialize(serializers.ModelSerializer):
    article_count = serializers.SerializerMethodField()

    def get_article_count(self, obj):
        return obj.category.filter(article_deleted=False).count()

    class Meta:
        model = models.CategoryModel
        fields = '__all__'


class TagSerialize(serializers.ModelSerializer):

    class Meta:
        model = models.TagModel
        fields = '__all__'


class ArticleSerialize(serializers.ModelSerializer):
    article_create_at = serializers.DateTimeField('%Y-%m-%d')
    category_title = serializers.CharField(source='category.category_title')
    nickname = serializers.CharField(source='user.nickname')
    # tags = serializers.ManyRelatedField(child_relation=models.ArticleModel.tag)
    # tags = TagSerialize(many=True)
    tags = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        # markdown.markdown()
        return markdown_detail(obj.article_content, )

    def get_tags(self, obj):
        return TagSerialize(instance=obj.tag, many=True).data

    class Meta:
        model = models.ArticleModel
        fields = '__all__'
