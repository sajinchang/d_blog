from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from mdeditor.fields import MDTextField


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


class ArticleModel(models.Model):
    """
    文章model
    """
    article_title = models.CharField('博客标题', max_length=128, unique=True)
    user = models.ForeignKey(to=User, verbose_name='所属用户')
    category = models.ForeignKey(to=CategoryModel, verbose_name='所属分类')
    tag = models.ManyToManyField(to=TagModel, verbose_name='所属标签')
    article_sort = models.IntegerField('排序', default=0)
    article_deleted = models.BooleanField('是否删除',
                                          choices=((True, '删除'), (False, '不删除')), default=False)
    article_content = MDTextField(verbose_name='内容')
    article_views = models.IntegerField('浏览量', default=0)
    article_create_at = models.DateTimeField('创建时间', auto_now_add=True)
    article_update_at = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.article_title

    class Meta:
        db_table = 'tbl_article'
        get_latest_by = 'create_at'
        verbose_name = '博客'
        verbose_name_plural = verbose_name
        indexes = [models.Index(fields=['article_title'])]

    def tags(self):
        """
        获取当前对象的tag
        """
        return [obj.tag_title for obj in self.tag.all()]

    def author(self):
        """
        获取博客作者
        """
        content = '<p style="color: %s">{}{}</p>'.format(self.user.last_name, self.user.first_name)
        if self.user.is_superuser:
            return content % 'red'
        return content % 'green'

    tags.short_description = '标签'
    tags.allow_tags = True

    author.short_description = '作者'
    author.allow_tags = True
