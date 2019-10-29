import logging
from django.contrib import admin

# Register your models here.
from blog import models

console = logging.getLogger('django')


class GlobalSetting():
    pass


@admin.register(models.TagModel)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_title', 'tag_create_at', 'tag_update_at')


@admin.register(models.CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_title',
                    'category_create_at', 'category_update_at']


@admin.register(models.ArticleModel)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['article_title', 'author', 'tags', 'category', 'article_deleted', 'article_sort',
                    'article_views', 'article_create_at', 'article_update_at']

    readonly_fields = ['article_views', 'user']
    # # 详细时间分层筛选　
    date_hierarchy = 'article_update_at'
    list_filter = ['user', 'category', 'tag', 'article_deleted']
    search_fields = ['article_title', ]
    list_editable = ['article_sort', 'article_deleted']
    # many to many 后台显示,
    # filter_vertical = ['tag']
    filter_horizontal = ['tag']
    ordering = ['-article_deleted']
    # fk_fields = ['user__first_name']
    # 每页数量
    list_per_page = 50
    # def add_view(self, request, form_url='', extra_context=None):
    # print(request.POST)

    # TODO 重写save方法，实现添加博客时自动添加作者，修改时不改变。
    # 重写get_queryset()方法，实现非高级管理员只可以查询自己所创作的博客
    # 重写delete方法，实现只修改deleted字段,并非真正的删除博客对象
    def get_queryset(self, request):
        """
        重写该方法,根据user权限返回博客,非高级管理员只显示自己创建的blog
        """
        query_set = super(ArticleAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            query_set = query_set.filter(user=request.user)
        return query_set

    # def add_view(self, request, form_url='', extra_context=None):

    def save_model(self, request, obj, form, change):
        """
        重写该方法, 实现新增时自动绑定 foreign key `user`
        """
        if not change:
            obj.user = request.user
        print(request.user.username)
        super(ArticleAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """
        删除model
        """
        pass


admin.site.site_header = '博客管理系统'
admin.site.site_title = '博客'
