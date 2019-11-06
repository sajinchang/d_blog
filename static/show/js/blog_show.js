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
    var $top = $('#top');

    $.get('/blog/tag/cache', {}, function (result) {
        console.log(result);

        if (result.code !== 200) {
            console.log('error');
            return false;
        }
        // 标签云
        $.each(result.data.tags_data, function (index, val) {
            $tag_cloud.append('<a href="/blog/tag/' + val.id + '">' + val.tag_title + '</a>');

        });

        // 类别
        $.each(result.data.category_data, function (index, val) {
            console.log(result.data.category_data);
            $category.append(' <li><a href="/blog/category/' + val.id + '">' + val.category_title +
                '（' + val.article_count + '）</a></li>')
        });

        // 推荐文章
        $.each(result.data.rcmd_article, function (index, val) {
            $rcmd_blog.append('<li><a href="/blog/' + val.id + '">' + val.article_title + '</a></li>');
        });
    });

    // top10 博客排行榜
    $.get('/blog/top/article', {}, function (result) {
        console.log(result);

        if (result.code !== 200) {
            console.log('error');
            return false;
        }
        $.each(result.data, function (index, val) {
            $top.append('<li><a href="/blog/' + val.id + '">' + val.article_title + '</a></li>')
        })
    })

});