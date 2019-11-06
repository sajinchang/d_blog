/****************************
 -*- coding: utf-8 -*-
 @Time    : 2019/11/5 下午10:01
 @Author  : SamSa
 @Email   : sajinde@qq.com
 @File    : gallery_rcmd.py
 @statement:
 ***************************/

$(function () {
    var $gallery_top = $('#gallery-top');
    $.get('/gallery/top', {}, function (result) {
        console.log(result);
        if (result.code !== 200){
            return false;
        }
        $.each(result.data, function (index, val) {
                    $gallery_top.append('<li><a href="/gallery/' + val.id +
                        '"><img src="' + val.gallery_img + '"></a></li>');

        });
    })
});