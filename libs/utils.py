# -*- coding: utf-8 -*-
# @Author  : SamSa
import logging
import os
import time
from uuid import uuid4
from hashlib import md5

from django.core.cache import cache
from django.core.paginator import Paginator
from django.core.paginator import InvalidPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage

inf = logging.getLogger('inf')


def upload_dir(instance, file):
    """
    自定义上传文件的路径
    :param file:
    :param instance:
    :return:
    """
    ext = os.path.splitext(file)[-1]
    filename = f'int{int(time.time())}{uuid4().hex[:10]}{ext}'
    return os.path.join(instance.__class__.__name__, filename)


def query_page(pre_page, current_page=1, pages=None, queryset=None, serialize=None):
    """
    queryset 对象分页
    :param pre_page: 每页显示数据
    :param current_page: 当前页码
    :param pages: 前端显示的页码list
    :param queryset: queryset 对象
    :param serialize: 序列化类
    :return:
    """
    if queryset is None:
        return None

    try:
        current_page = int(current_page)
    except TypeError:
        current_page = 1

    # 开始分页, 传入queryset和每页显示数量
    paginator = Paginator(queryset, pre_page)
    err = ''
    try:
        page = paginator.page(current_page)
    except (EmptyPage, PageNotAnInteger, InvalidPage):
        err = '已经是最后一页了'
        page = paginator.page(paginator.num_pages)
        current_page = paginator.num_pages

    # 如果当前页总页数一半 + 1
    if current_page < int(pages / 2) + 1:
        # 如果总页数小于等于配置显示的页码
        if paginator.num_pages <= pages:
            page_list = range(1, paginator.num_pages + 1)

        else:
            page_list = range(1, pages + 1)
    # 如果当前页大于等于配置显示页码的一半 + 1, 并且当前页小于等于总页数减去配置显示的一半
    elif (current_page >= int(pages / 2) + 1) and (current_page <= paginator.num_pages - int(pages / 2)):
        page_list = range(current_page - int(pages / 2), current_page + int(pages / 2))

    else:
        page_list = range(paginator.num_pages - pages + 1, paginator.num_pages + 1)
    previous = page.has_previous()
    next = page.has_next()
    result = {
        'error': err,
        'total_data': queryset.count(),
        'previous_url': current_page - 1 if previous else None,
        'previous': previous,
        'next': next,
        'next_url': current_page + 1 if next else None,
        'data': serialize(instance=page.object_list, many=True).data,
        'current_page': current_page,
        'page_nums': list(page_list),
        'total_page': len(queryset) / pre_page if len(queryset) % pre_page == 0 else int(len(queryset) / pre_page) + 1
    }

    return result


def split_list_n_list(origin, n):
    """
    列表平均切分为几个新的列表
    :param origin: 源列表
    :param n: 切分为几个
    :return:
    """
    if len(origin) % n == 0:
        cnt = len(origin) // n
    else:
        cnt = len(origin) // n + 1
    for i in range(n):
        yield origin[i * cnt:(i + 1) * cnt]


def get_md5(string):
    """
    获取md5值
    :param string:
    :return:
    """
    m = md5(string.encode('utf8'))
    return m.hexdigest()


def set_cache(expiration=5 * 60):
    """
    缓存装饰器
    :param expiration: 过期时间
    :return:
    """

    def wrapper(func):
        def inner(*args, **kwargs):
            key = repr((func.__name__, args, kwargs))
            key = get_md5(key)
            res = cache.get(key)
            print(res)
            if not res:
                res = func(*args, **kwargs)
                cache.set(key, res, expiration)
                print(key)

                inf.info('cache_decorator get cache:%s key:%s' % (func.__name__, key))
            return res

        return inner

    return wrapper


def limit_verify(limit, default=10):
    """
    :param limit:
    :param default:
    :return:
    """
    try:
        limit = int(limit)
    except ValueError:
        limit = default
    if limit > default:
        limit = default

    return limit
