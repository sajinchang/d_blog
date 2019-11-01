from abc import ABC

from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
    PermissionsMixin

from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('请输入用户名')
        if not password:
            raise ValueError('请输入密码')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password, **extra_fields):
        return self._create_user(username, password=password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must have is_superuser=True')

        if extra_fields.get('is_active') is not True:
            raise ValueError('superuser must have is_active=True')

        return self._create_user(username, password, **extra_fields)


class UserModel(AbstractBaseUser, PermissionsMixin):
    password = models.CharField('密码', max_length=128,
                                help_text=mark_safe('<a href="/test">修改密码</a>'))
    # is_staff = models.BooleanField('是否有权限访问后台', default=True)
    nickname = models.CharField('昵称', max_length=128)
    username = models.CharField('用户名', max_length=128, unique=True)
    email = models.CharField('邮箱', max_length=64, unique=True)
    is_active = models.BooleanField('是否激活', default=True)
    is_admin = models.BooleanField('是否为管理员', default=True)
    last_login = models.DateTimeField('最近登录', blank=True, null=True)
    create_at = models.DateTimeField('创建时间', auto_now_add=True)
    update_at = models.DateTimeField('更新时间', auto_now=True)

    # identifier = models.CharField(max_length=40, unique=True)
    # REQUIRED_FIELDS = ['username', 'password']
    USERNAME_FIELD = 'username'

    objects = UserManager()

    def get_full_name(self):
        return self.nickname

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        super().has_module_perms(app_label)

    @property
    def is_staff(self):
        # return self.is_admin  #这个必须是指定admin才能登陆Django admin后台
        return self.is_active  # 这个只要用户时is_active的即可登陆Django admin后台

    class Meta:
        db_table = 'tbl_account'
        indexes = [models.Index(fields=['username', 'email'])]
        verbose_name = '用户'
        verbose_name_plural = verbose_name
