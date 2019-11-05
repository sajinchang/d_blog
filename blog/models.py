from django.conf import settings
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from mdeditor.fields import MDTextField
from stdimage import StdImageField

from libs.redis_cache import RankArticle
from libs.utils import upload_dir


class TagModel(models.Model):
    """
    标签model
    """
    tag_title = models.CharField('标签名称', max_length=128, unique=True)
    tag_create_at = models.DateTimeField('创建时间', auto_now_add=True)
    tag_update_at = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.tag_title

    class Meta:
        db_table = 'tbl_tag'
        get_latest_by = 'create_at'
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class CategoryModel(models.Model):
    """
    类别model
    """
    category_title = models.CharField('类别名称', max_length=128, unique=True)
    category_create_at = models.DateTimeField('创建时间', auto_now_add=True)
    category_update_at = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.category_title

    class Meta:
        db_table = 'tbl_category'
        get_latest_by = 'create_at'
        verbose_name = '分类'
        verbose_name_plural = verbose_name


class ArticleManager(models.Manager):
    """
    重写ArticleModel的模型管理器, 每一次浏览对浏览量加1
    """

    def get(self, *args, **kwargs):
        obj = super().get(*args, **kwargs)
        obj.article_views += 1
        obj.save()
        return obj


class ArticleModel(models.Model):
    """
    文章model
    """
    article_title = models.CharField('博客标题', max_length=128, unique=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='所属用户')
    category = models.ForeignKey(to=CategoryModel, verbose_name='所属分类',
                                 null=True, blank=True,
                                 related_name='category',
                                 on_delete=models.SET_NULL)
    tag = models.ManyToManyField(to=TagModel, verbose_name='所属标签', related_name='tag')
    article_sort = models.IntegerField('排序', default=0)
    article_deleted = models.BooleanField('是否删除',
                                          choices=((True, '删除'), (False, '不删除')),
                                          default=False)
    article_img = StdImageField('封面图片', upload_to=upload_dir,
                                variations={'thumbnail': (100, 75)},
                                blank=True, null=True)
    article_commend = models.TextField('简介', null=True, blank=True)
    article_content = MDTextField(verbose_name='内容', null=True, blank=True)
    article_views = models.IntegerField('浏览量', default=0)
    article_create_at = models.DateTimeField('创建时间', auto_now_add=True)
    article_update_at = models.DateTimeField('更新时间', auto_now=True)

    objects = ArticleManager()

    def __str__(self):
        return self.article_title

    class Meta:
        db_table = 'tbl_article'
        get_latest_by = 'create_at'
        verbose_name = '博客'
        ordering = ['article_views']
        verbose_name_plural = verbose_name
        indexes = [models.Index(fields=['article_title'])]

    def tags(self):
        """
        获取当前对象的tag
        """
        if not hasattr(self, '_tags'):
            self._tags = [obj.tag_title for obj in self.tag.all()]

        return self._tags

    @property
    def get_tags(self):
        if not hasattr(self, '_get_tags'):
            self._get_tags = self.tag.all()

        return self._get_tags

    def author(self):
        """
        获取博客作者
        """
        content = '<p style="color: %s">{}</p>'.format(self.user.nickname)
        if self.user.is_superuser:
            return content % 'red'
        return content % 'green'

    tags.short_description = '标签'
    tags.allow_tags = True

    author.short_description = '作者'
    author.allow_tags = True

    def img(self):
        if hasattr(self.article_img, 'thumbnail'):
            return u'<img src="%s" />' % (self.article_img.thumbnail.url)
        return '上传图片'

    img.short_description = '封面图片'
    img.allow_tags = True


@receiver([pre_delete], sender=ArticleModel)
def delete_article_img(sender, instance, **kwargs):
    instance.article_img.delete(False)


@receiver([pre_delete], sender=ArticleModel)
def delete_rank_article(sender, instance, **kwargs):
    """
    文章删除时,删除缓存中的排行榜数据
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    RankArticle.del_pk(instance.pk)
