from django.contrib.admin.models import LogEntry
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AdminPasswordChangeForm
from django.contrib.admin.models import LogEntry, DELETION
from django.urls import get_urlconf
from django.utils.html import escape
from django.core.urlresolvers import reverse

from .models import UserModel as MyUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('username', 'nickname', 'email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("两次密码不匹配")

        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('username', 'nickname', 'email', 'password', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'nickname', 'email',
                    'is_active', 'is_admin', 'create_at',
                    'update_at')
    list_editable = ('is_active', 'is_admin')
    list_filter = ('is_admin',)
    readonly_fields = ('is_superuser', 'password', 'last_login')
    fieldsets = (
        (None, {'fields': ('username', 'nickname',
                           'email', 'password', 'last_login')}),

        ('权限',
         {'fields': ('is_superuser', ('is_admin', 'is_active'), 'user_permissions')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')}
         ),
    )
    search_fields = ('email', 'username')
    ordering = ('email', 'username')
    filter_horizontal = ('user_permissions',)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    readonly_fields = [field.attname for field in LogEntry._meta.fields]
    readonly_fields += ['content_type', 'user']

    list_filter = ['user', 'content_type', 'action_flag']

    search_fields = ['object_repr', 'change_message']

    list_display = ['action_time', 'user', 'content_type', 'object_link',
                    'action_flag', 'change_message', '__str__']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True
        # return request.user.is_superuser and request.method != 'POST'

    def has_module_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return False
        # if request.user.is_superuser:
        #     return True
        # return super().has_delete_permission(request, obj)

    def object_link(self, obj):
        """
        对应所操作对象的链接
        :param obj:
        :return:
        """
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = u'<a href="%s">%s</a>' % (reverse('admin:%s_%s_change' % (ct.app_label, ct.model),
                                                     args=[obj.object_id]), escape(obj.object_repr),)
        return link

    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'所操作对象'

    def queryset(self, request):
        """
        1. 因为select_related()总是在单次SQL查询中解决问题，而prefetch_related()会对每个相关表进行SQL查询，
        因此select_related()的效率通常比后者高。
        2. 鉴于第一条，尽可能的用select_related()解决问题。只有在select_related()不能解决问题的时候再去想
        prefetch_related()。
        3. 你可以在一个QuerySet中同时使用select_related()和prefetch_related()，从而减少SQL查询的次数。
        4. 只有prefetch_related()之前的select_related()是有效的，之后的将会被无视掉。
        :param request:
        :return:
        """
        return super(LogEntryAdmin, self).queryset(request).prefetch_related('content_type')

    def get_actions(self, request):
        """
        去除默认的delete_selected action
        :param request:
        :return:
        """
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            actions.pop('delete_selected')
        return actions


admin.site.unregister(Group)
