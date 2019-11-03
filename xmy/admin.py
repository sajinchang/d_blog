from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from xmy.models import AlbumModel, GalleryModel

# Register your models here.


class ImageInline(admin.TabularInline):
    model = AlbumModel


@admin.register(GalleryModel)
class GalleryAdmin(ImportExportActionModelAdmin):
    list_display = ['gallery_title', 'image_img', 'gallery_deleted',
                    'gallery_create_at', 'gallery_update_at', 'get_status']
    search_fields = ['gallery_title']
    date_hierarchy = 'gallery_update_at'
    list_editable = ['gallery_deleted']
    ordering = ['gallery_deleted']
    inlines = [
        ImageInline
    ]

    def delete_model(self, request, obj):
        """
        删除model
        """
        obj.gallery_deleted = True
        obj.save()

    def get_actions(self, request):
        """
        去除默认的删除按钮 delete_selected action
        """
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if 'delete_selected' in actions:
                actions.pop('delete_selected')
        return actions

    def get_status(self, obj):
        if obj.gallery_deleted is True:
            return '<b style="color: red">不显示</b>'

        return '<b style="color: green">显示</b>'

    get_status.short_description = '当前状态'
    get_status.allow_tags = True


@admin.register(AlbumModel)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['gallery', 'image_img', 'album_deleted',
                    'album_create_at', 'album_update_at', 'get_status']

    search_fields = ['gallery__gallery_title']
    list_editable = ['album_deleted']
    list_filter = ('album_deleted', )

    def delete_model(self, request, obj):
        """
        删除model
        """
        obj.album_deleted = True
        obj.save()

    def get_actions(self, request):
        """
        去除默认的删除按钮 delete_selected action
        """
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if 'delete_selected' in actions:
                actions.pop('delete_selected')
        return actions

    def get_status(self, obj):
        if obj.album_deleted is True:
            return '<b style="color: red">不显示</b>'

        return '<b style="color: green">显示</b>'

    get_status.short_description = '当前状态'
    get_status.allow_tags = True
