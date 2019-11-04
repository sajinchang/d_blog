/****************************
 -*- coding: utf-8 -*-
 @Time    : 2019/11/4 下午4:42
 @Author  : SamSa
 @Email   : sajinde@qq.com
 @File    : blog_show.py
 @statement:
 ***************************/

$(function () {

    var $tag_cloud = $('#tag_cloud');
    var $category = $('#category');
    var $rcmd_blog = $('#rcmd_blog');

    $.get('/blog/tag/cache', {}, function (result) {
        // 标签云
        $.each(result.data.tags_data, function (index, val) {
            $tag_cloud.append('<a>' + val.tag_title + '</a>');

        });

        // 类别
        $.each(result.data.category_data, function (index, val) {
            console.log(result.data.category_data);
            $category.append(' <li><a href="/">' + val.category_title +
                '（' + val.article_count + '）</a></li>')
        });

        // 推荐文章
        $.each(result.data.rcmd_article, function (index, val) {
            $rcmd_blog.append('<li><a href="/blog/' + val.id +'">'+ val.article_title+'</a></li>');
        });
    })

});