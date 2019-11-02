# -*- coding: utf8 -8-
# @Author: SamSa

from django.db import models


def to_dict(self, *exclude):
    """
    :param: exclude: 无需返回的字段
    :return     type: dict
    """

    attname_dict = dict()
    for field in self._meta.fields:
        if field.attname not in exclude:
            attname_dict[field.attname] = getattr(self, field.attname)
    return attname_dict


def patch_model():
    """
    动态给model添加函数
    """
    models.Model.to_dict = to_dict
