from django.contrib import admin

# Register your models here.
from blog import models


# @admin.register(models.TagModel)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag_title', 'tag_create_at', 'tag_update_at')

admin.site.register(models.TagModel, TagAdmin)
admin.site.register(models.CategoryModel)
admin.site.register(models.ArticleModel)