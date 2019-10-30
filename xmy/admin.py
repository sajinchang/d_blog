from django.contrib import admin
from xmy.models import GalleryModel
from xmy.models import AlbumModel
# Register your models here.


@admin.register(GalleryModel)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['gallery_title', 'image_img',
                    'gallery_create_at', 'gallery_update_at']
    search_fields = ['gallery_title']
    date_hierarchy = 'gallery_update_at'


@admin.register(AlbumModel)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['gallery', 'image_img',
                    'album_create_at', 'album_update_at']

    search_fields = ['gallery__gallery_title']
