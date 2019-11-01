from django.contrib.admin.models import LogEntry
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AdminPasswordChangeForm
from django.contrib.auth.forms import PasswordChangeForm
# from django.contrib.contenttypes.models import ContentType
# from django.utils.encoding import force_unicode

from .models import UserModel as MyUser


# class PwdChangeForm(forms.Form):
#     old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput)
#
#     password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)
#
#     # use clean methods to define custom validation rules
#
#     def clean_password1(self):
#         password1 = self.cleaned_data.get('password1')
#
#         if len(password1) < 6:
#             raise forms.ValidationError("your password is too short")
#         elif len(password1) > 20:
#             raise forms.ValidationError("your password is too long")
#
#         return password1
#
#     def clean_password2(self):
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')
#
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Password mismatch Please enter again")
#
#         return password2


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

    # password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('username', 'nickname', 'email', 'password', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


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


# # 文件最下方增加
# @admin.register(LogEntry)
# class LogEntryAdmin(admin.ModelAdmin):
#     list_display = ['object_repr',
#                     'action_flag', 'user', 'change_message']
#
#     def log_addition(self, request, object):
#         """
#         Log that an object has been successfully added.
#         The default implementation creates an admin LogEntry object.
#         """
#         from django.contrib.admin.models import LogEntry, ADDITION
#         LogEntry.objects.log_action(
#             user_id=request.user.pk,
#             content_type_id=ContentType.objects.get_for_model(object).pk,
#             object_id=object.pk,
#             object_repr=force_unicode(object),
#             action_flag=ADDITION
#         )
#
#     def log_change(self, request, object, message):
#         """
#         Log that an object has been successfully changed.
#         The default implementation creates an admin LogEntry object.
#         """
#         from django.contrib.admin.models import LogEntry, CHANGE
#         LogEntry.objects.log_action(
#             user_id=request.user.pk,
#             content_type_id=ContentType.objects.get_for_model(object).pk,
#             object_id=object.pk,
#             object_repr=force_unicode(object),
#             action_flag=CHANGE,
#             change_message=message
#         )
#
#     def log_deletion(self, request, object, object_repr):
#         """
#         Log that an object will be deleted. Note that this method is called
#         before the deletion.
#         The default implementation creates an admin LogEntry object.
#         """
#         from django.contrib.admin.models import LogEntry, DELETION
#         LogEntry.objects.log_action(
#             user_id=request.user.id,
#             content_type_id=ContentType.objects.get_for_model(self.model).pk,
#             object_id=object.pk,
#             object_repr=object_repr,
#             action_flag=DELETION
#         )

admin.site.register(MyUser, MyUserAdmin)
admin.site.unregister(Group)
