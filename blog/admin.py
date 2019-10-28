from django.contrib import admin

# Register your models here.
from blog import models


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

    readonly_fields = ['article_views', ]
    date_hierachy = ['update_at']
    list_filter = ['article_title', 'user', 'category', 'tag', 'article_deleted']
    search_fields = ['article_title', ]
    list_editable = ['article_sort', 'article_deleted']
    # many to many 后台显示,
    filter_vertical = ['tag'] 

admin.site.site_header = '博客管理系统'
admin.site.site_title = '博客'
# admin.site.register(models.TagModel, TagAdmin)
# admin.site.register(models.CategoryModel, CategoryAdmin)
# admin.site.register(models.ArticleModel, ArticleAdmin)