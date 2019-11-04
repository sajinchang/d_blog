# -*- coding: utf-8 -*-
# @Author  : SamSa
from django.templatetags.cache import Node


class TagCacheNode(Node):
    """自定义模板碎片缓存"""
    def __init__(self, nodelist, expire_time_var, fragment_name,
                 vary_on, cache_name, fun=None):
        self.nodelist =nodelist
        self.expire_time_var = expire_time_var
        self.fragment_name = fragment_name
        self.vary_on = vary_on
        self.cache_name = cache_name
        self.fun = fun

    # def
