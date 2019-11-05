# -*- coding: utf-8 -*-
# @Author  : SamSa
# redis连接
from redis import Redis
from django.conf import settings

from blog import models
from d_blog import keys

rds = Redis(**settings.REDIS)


class RankArticle(object):
    """
    博客文章实现排行榜
    """
    KEY = keys.RANK_ARTICLE

    @classmethod
    def add_score(cls, pk):
        """
        分数增长
        :param pk:
        :param key:
        :return:
        """
        # rds.zadd(cls.KEY, {pk: 1})
        rds.zincrby(cls.KEY, 1, pk)

    @classmethod
    def del_pk(cls, pk):
        """
        删除某个值
        :param pk:
        :return:
        """
        rds.zrem(cls.KEY, str(pk))

    @classmethod
    def get_top_article(cls, num):
        """
        获取排行榜
        :param num: 取前多少位
        :return: queryset 对象
        """
        # withscores=True表示倒序
        top_data = rds.zrevrange(cls.KEY, 0, num - 1, withscores=True)

        art_id_list = [int(art_id) for art_id, score in top_data]

        # 查询数据
        article_list = models.ArticleModel.objects.filter(id__in=art_id_list)
        articles = sorted(article_list, key=lambda article: art_id_list.index(article.pk))
        return articles
