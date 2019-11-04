# -*- coding: utf-8 -*-
# @Author  : SamSa
from django.core import cache
from django.conf import settings

from blog.models import TagModel, CategoryModel, ArticleModel
from libs.utils import set_cache
from serialize.blog_serialize import TagSerialize, CategorySerialize, ArticleSerialize


@set_cache(key='%s-%s' % (settings.SECRET_KEY, 'get_category_cache'))
def get_category_cache():
    tags_queryset = TagModel.objects.all()
    tags_data = TagSerialize(instance=tags_queryset, many=True).data

    category_queryset = CategoryModel.objects.all()
    category_data = CategorySerialize(instance=category_queryset, many=True).data

    rcmd_article = ArticleModel.objects.filter(article_deleted=False).order_by('article_sort')[:10]
    article_data = ArticleSerialize(instance=rcmd_article, many=True).data
    data = {
        'tags_data': tags_data,
        'category_data': category_data,
        'rcmd_article': article_data,
    }
