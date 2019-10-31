from django.db import models
from stdimage import StdImageField
# Create your models here.


class GalleryModel(models.Model):
    """
    相册
    """
    gallery_title = models.CharField('标题', max_length=128, unique=True,
                                     help_text='相册标题应该是唯一的')
    gallery_img = StdImageField(upload_to='media/', blank=True, null=True,
                                variations={'thumbnail': (100, 75)},
                                verbose_name=u'封面图片')
    gallery_comment = models.TextField('简介说明', null=True, blank=True)
    gallery_create_at = models.DateTimeField('创建时间', auto_now_add=True)
    gallery_update_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'tbl_gallery'
        verbose_name = '相册'
        verbose_name_plural = verbose_name

    def image_img(self):
        if hasattr(self.gallery_img, 'thumbnail'):
            return u'<img src="%s" />' % (self.gallery_img.thumbnail.url)
        return '上传图片'

    image_img.short_description = '封面图片'
    image_img.allow_tags = True

    def __str__(self):
        return self.gallery_title


class AlbumModel(models.Model):
    """
    具体相册多图
    """
    album_img = StdImageField(upload_to='media/', null=True, blank=True,
                              variations={'thumbnail': (100, 75)},
                              verbose_name='图片')
    gallery = models.ForeignKey(GalleryModel, verbose_name='所属相册', null=True, blank=True,
                                on_delete=models.SET_NULL)

    album_create_at = models.DateTimeField('创建时间', auto_now_add=True)
    album_update_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'tbl_album'
        verbose_name = '相册图片'
        verbose_name_plural = verbose_name

    def image_img(self):
        if hasattr(self.album_img, 'thumbnail'):
            return u'<img src="%s" />' % (self.album_img.thumbnail.url)
        return '上传图片'

    image_img.short_description = '图片'
    image_img.allow_tags = True

    def __str__(self):
        return '相册图片'
