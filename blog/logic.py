# -*- coding: utf-8 -*-
# @Author  : SamSa
from django.core import cache


def set_cache(key):
    def wrapper(func):
        def inner(*args, **kwargs):
            res = func(*args, **kwargs)
            cache.cache(key, res, 5 * 60)

        return inner

    return wrapper
