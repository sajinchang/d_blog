from django.shortcuts import render

# Create your show_api here.
from django.urls import reverse

from blog.models import ArticleModel
from libs.http import render_json
from libs.redis_cache import RankArticle
from libs.utils import query_page
from libs.view import BaseView
from serialize.blog_serialize import ArticleSerialize
from . import logic


class BlogShowView(BaseView):
    def get(self, request, pk):
        obj = ArticleModel.objects.get(pk=pk)
        # 排行榜分数+1
        RankArticle.add_score(pk=obj.pk)
        data = ArticleSerialize(instance=obj, many=False).data
        # return render_json(data=data)
        return render(request, 'show/info.html', context=data)


def tag_cache(request):
    """
    标签云缓存
    :param request:
    :return:
    """
    tags_data = logic.get_tag_cache()
    category_data = logic.get_category_cache()
    article_data = logic.get_rcmd_article()
    data = {
        'tags_data': tags_data,
        'category_data': category_data,
        'rcmd_article': article_data,
    }
    return render_json(data=data)


def top_article(request):
    """
    获取blog排行榜
    :param request:
    :return:
    """
    articles = RankArticle.get_top_article(num=10)
    data = ArticleSerialize(instance=articles, many=True).data
    return render_json(data=data)


class CategoryTagView(BaseView):
    """
    根据分类获取blog
    """

    def get(self, request,tag_category, pk):
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        if tag_category.__eq__('tag'):
            articles = ArticleModel.objects.filter(tag__id=pk, article_deleted=False).prefetch_related('tag__tag')
        elif tag_category.__eq__('category'):
            articles = ArticleModel.objects.filter(category_id=pk, article_deleted=False)
        else:
            articles = ArticleModel.objects.filter(article_deleted=False)
        result = query_page(pre_page=limit, pages=9, current_page=page,
                            queryset=articles, serialize=ArticleSerialize)
        url = reverse('blog:category_tag', kwargs={'pk': pk, 'tag_category': tag_category})
        result['url'] = url
        return render(request, 'show/list.html', context=result)


class BlogView(BaseView):
    """
    博客列表查询
    """

    def get(self, request):
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        queryset = ArticleModel.objects.filter(article_deleted=False)
        result = query_page(pre_page=limit, pages=9, current_page=page,
                            queryset=queryset, serialize=ArticleSerialize)
        url = reverse('blog:blog_list')
        result['url'] = url
        return render(request, 'show/list.html', context=result)
