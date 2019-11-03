from django.shortcuts import render

from libs import view
from libs.http import render_json
from libs.utils import query_page, split_list_n_list
from serialize.gallery_serialize import GallerySerialize
from .models import GalleryModel


class GalleryView(view.BaseView):

    def get(self, request):
        """
        相册页面查询
        :param request:
        :return:
        """
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 24)
        query_set = GalleryModel.objects.filter(gallery_deleted=False)
        result = query_page(pre_page=limit, current_page=page,
                            serialize=GallerySerialize, pages=9, queryset=query_set)
        result.update({'data': list(split_list_n_list(result['data'], 4))})
        return render(request, 'show/share.html', context=result)
        # return render_json(data=result)


class GalleryShowView(view.BaseView):

    def get(self, request, pk):
        """

        :param request:
        :param pk:
        :return:
        """
        obj = GalleryModel.objects.get(pk=pk)
        data = GallerySerialize(instance=obj, many=False).data
        return render(request, 'show/infopic.html', context=data)
        # return render_json(data=data)

