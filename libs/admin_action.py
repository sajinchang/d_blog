# -*- coding: utf-8 -*-
# @Author  : SamSa
from django.core import serializers
from django.http import HttpResponse

from libs.redis_cache import RankArticle


def export_as_json(modeladmin, request, queryset):
    """
    数据导处为json格式
    :param modeladmin:  modeladmin class
    :param request:     request请求对象
    :param queryset:    数据库queryset对象
    :return:
    """
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response


export_as_json.short_description = '数据导出为json'


def delete_selected_queryset(modeladmin, request, queryset):
    """
    选中删除
    :param modeladmin:
    :param request:
    :param queryset:
    :return:
    """
    queryset.update(article_deleted=True)
    # 删除文章, 排行榜id删除
    list(map(RankArticle.del_pk, [obj.pk for obj in queryset]))


delete_selected_queryset.short_description = '逻辑删除所选内容'
