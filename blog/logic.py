# -*- coding: utf-8 -*-
# @Author  : SamSa
from django.conf import settings

from blog import models
from libs.utils import set_cache
from serialize import blog_serialize


@set_cache(key='%s-%s' % (settings.SECRET_KEY, 'get_category_cache'))
def get_category_cache():
    """
    获取分类缓存
    :return:
    """
    category_queryset = models.CategoryModel.objects.all()
    category_data = blog_serialize.CategorySerialize(instance=category_queryset, many=True).data

    return category_data


@set_cache(key='%s-%s' % (settings.SECRET_KEY, 'get_tag_cache'))
def get_tag_cache():
    """
    获取标签云缓存
    :return:
    """
    tags_queryset = models.TagModel.objects.all()
    tags_data = blog_serialize.TagSerialize(instance=tags_queryset, many=True).data
    return tags_data


@set_cache(key='%s-%s' % (settings.SECRET_KEY, 'get_rcmd_article_cache'))
def get_rcmd_article():
    """
    获取推荐文章缓存
    :return:
    """
    rcmd_article = models.ArticleModel.objects.filter(
        article_deleted=False).order_by('article_sort')[:10]
    article_data = blog_serialize.ArticleSerialize(instance=rcmd_article, many=True).data
    return article_data
