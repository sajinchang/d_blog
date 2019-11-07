# -*- coding: utf-8 -*-
# @Author  : SamSa

from haystack import indexes

from .models import ArticleModel


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
   text = indexes.CharField(document=True, use_template=True)

   def get_model(self):
       return ArticleModel

   def get_queryset(self, using=None):
       return self.get_model().objects.filter(article_deleted=False)