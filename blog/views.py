from django.shortcuts import render

# Create your views here.
from blog.models import ArticleModel, TagModel, CategoryModel
from libs.http import render_json
from libs.view import BaseView
from serialize.blog_serialize import ArticleSerialize, TagSerialize, CategorySerialize


class BlogShowView(BaseView):
    def get(self, request, pk):
        obj = ArticleModel.objects.get(pk=pk)
        data = ArticleSerialize(instance=obj, many=False).data
        return render(request, 'show/info.html', context=data)


def tag_cache(request):
    """
    标签云缓存
    :param request:
    :return:
    """
    # tags_queryset = TagModel.objects.all()
    # tags_data = TagSerialize(instance=tags_queryset, many=True).data
    #
    # category_queryset = CategoryModel.objects.all()
    # category_data = CategorySerialize(instance=category_queryset, many=True).data
    #
    # rcmd_article = ArticleModel.objects.filter(article_deleted=False).order_by('article_sort')[:10]
    # article_data = ArticleSerialize(instance=rcmd_article, many=True).data
    # data = {
    #     'tags_data': tags_data,
    #     'category_data': category_data,
    #     'rcmd_article': article_data,
    # }
    return render_json(data=data)
    # return render(request, 'show/info.html', context={'data': data})
