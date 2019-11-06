/****************************
 -*- coding: utf-8 -*-
 @Time    : 2019/11/6 下午2:42
 @Author  : SamSa
 @Email   : sajinde@qq.com
 @File    : nav.js.py
 @statement:
 ***************************/

$(function () {
    // 导航栏样式
    var $nav = $('#nav');
    var $a = $nav.find('a');
    // 获取当前页面的url
    var href = window.location.href;
    // 遍历查找到的a连接
    $.each($a, function (index, v) {
        if(href === v.href){
            $(v).attr('id', 'selected');
        }
    })
});