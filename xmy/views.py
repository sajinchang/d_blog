import logging

from django.http import Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

from d_blog import keys
from d_blog.keys import LOGIN_URL
from libs import view, form
from libs.http import render_json
from libs import utils
from serialize.gallery_serialize import GallerySerialize
from xmy.models import GalleryLikeModel
from .models import GalleryModel

err = logging.getLogger('err')


class GalleryView(view.BaseView):
    @method_decorator(login_required(login_url=LOGIN_URL))
    def get(self, request):
        """
        相册页面查询
        :param request:
        :return:
        """
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 24)
        limit = utils.limit_verify(limit, default=24)
        query_set = GalleryModel.objects.filter(gallery_deleted=False)
        result = utils.query_page(pre_page=limit, current_page=page,
                                  serialize=GallerySerialize, pages=9, queryset=query_set)
        result.update({'data': list(utils.split_list_n_list(result['data'], 4))})
        return render(request, 'show/share.html', context=result)


class GalleryShowView(view.BaseView):
    @method_decorator(login_required(login_url=LOGIN_URL))
    def get(self, request, pk):
        """
        :param request:
        :param pk:
        :return:
        """
        # obj = get_object_or_404(GalleryModel, pk=pk)
        try:
            obj = GalleryModel.objects.get(pk=pk)
        except GalleryModel.DoesNotExist:
            raise Http404
        data = GallerySerialize(instance=obj, many=False).data
        return render(request, 'show/infopic.html', context=data)


class GalleryTopView(view.BaseView):
    @method_decorator(cache_page(60 * 5))
    def get(self, request):
        queryset = GalleryModel.objects.filter(
            gallery_deleted=False).order_by('gallery_sort')[:6]
        result = GallerySerialize(instance=queryset, many=True).data
        return render_json(data=result)


class GalleryLikeView(view.BaseView):
    """相册点赞视图"""

    def post(self, request):
        f = form.LikeForm(request.POST)
        if f.is_valid():

            try:
                obj = GalleryLikeModel.objects.get(gallery_id=f.cleaned_data['pk'])
            except (GalleryLikeModel.DoesNotExist, ValueError) as e:
                err.error(e)
                return render_json(code=keys.SERVER_ERROR, msg='点赞失败')
            else:
                obj.click_num += 1
                obj.save()

            return render_json()
        return render_json(code=keys.FORM_ERROR, msg=f.errors)
