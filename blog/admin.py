import logging

from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin

# Register your models here.
from blog import models
from libs import admin_action

console = logging.getLogger('django')


@admin.register(models.TagModel)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_title', 'tag_create_at', 'tag_update_at')


@admin.register(models.CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_title',
                    'category_create_at', 'category_update_at']


class ProxyResource(resources.ModelResource):
    class Meta:
        model = models.ArticleModel


@admin.register(models.ArticleModel)
class ArticleAdmin(ImportExportActionModelAdmin):
    resources_class = ProxyResource
    list_display = ['article_title', 'author', 'tags', 'category', 'article_deleted', 'article_sort',
                    'article_views', 'article_create_at', 'article_update_at', 'get_status']

    readonly_fields = ['article_views', 'user']
    # # 详细时间分层筛选　
    date_hierarchy = 'article_update_at'
    list_filter = ['user', 'category', 'tag', 'article_deleted']
    # 模糊搜索
    search_fields = ['article_title', 'user__first_name',
                     'user__last_name', 'user__username']
    # 界面可编辑
    list_editable = ['article_sort', 'article_deleted']
    # many to many 后台显示,
    # filter_vertical = ['tag']
    filter_horizontal = ['tag']
    ordering = ['article_deleted']
    # fk_fields = ['user__first_name']
    # 每页数量
    list_per_page = 50

    # 详情页显示
    fieldsets = (
        ('基本信息', {
            'fields': ('article_title', ('category', 'tag'),
                       ('article_sort', 'article_deleted'),
                       'article_content')
        }),
        ('其他', {
            'classes': ('extrapretty',),  # 直接显示
            # 'classes': ('collapse',), # 折叠
            'fields': ('article_views', 'user')
        }),
    )
    # 添加自定义选中动作
    actions = [admin_action.export_as_json,
               admin_action.delete_selected_queryset]

    def get_queryset(self, request):
        """
        重写该方法,根据user权限返回博客,非高级管理员只显示自己创建的blog
        """
        query_set = super(ArticleAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            query_set = query_set.filter(user=request.user)
        return query_set

    def save_model(self, request, obj, form, change):
        """
        重写该方法, 实现新增时自动绑定 foreign key `user`
        """
        if not change:
            obj.user = request.user
        super(ArticleAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """
        删除model
        """
        obj.article_deleted = True
        obj.save()

    def get_actions(self, request):
        """
        去除默认的delete_selected action
        :param request:
        :return:
        """
        actions = super(ArticleAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            if 'delete_selected' in actions:
                actions.pop('delete_selected')
        return actions

    def get_status(self, obj):
        if obj.article_deleted is True:
            return '<b style="color: red">不显示</b>'
        else:
            return '<b style="color: green">显示</b>'

    get_status.short_description = '当前状态'
    get_status.allow_tags = True


admin.site.site_header = '博客管理系统'
admin.site.site_title = '博客'
# admin.site.disable_action('delete_selected')
