# -*- coding: utf-8 -*-
# @Author  : SamSa
from django import forms


class LikeForm(forms.Form):
    """点赞表单验证"""
    pk = forms.IntegerField(min_value=1, required=True, error_messages={'required': '必须为大于0的整数'})

    # def clean_pk(self):
    #     pk = self.cleaned_data['pk']
