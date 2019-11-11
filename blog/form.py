# -*- coding: utf-8 -*-
# @Author  : SamSa

from django import forms

from blog.models import CommentModel


class CommentForm(forms.ModelForm):
    """评论表单"""

    class Meta:
        model = CommentModel
        fields = [
            'article', 'parent', 'info', 'email'
        ]
        error_messages = {
            'article': {'required': '文章不可以为空'},
            'info': {'required': '评论内容不能为空'}
        }
