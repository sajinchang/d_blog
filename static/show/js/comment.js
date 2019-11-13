/****************************
 -*- coding: utf-8 -*-
 @Time    : 2019/11/12 上午10:45
 @Author  : SamSa
 @Email   : sajinde@qq.com
 @File    : comment.js
 @statement:
 ***************************/

layui.use(['layer', 'layedit', 'form'], function () {
    var form = layui.form,
        layedit = layui.layedit,
        layer = layui.layer;


    // 评论回复
    $('.reply').click(function () {
        var reply = layer.open({
            title: '评论',
            type: 1,
            area: ['1000px', '500px'],
            content: $('#comment-form') //这里content是一个DOM，注意：最好该元素要存放在body最外层，否则可能被其它的相对元素所影响
        });

        // layui富文本编辑器创建
        layedit_build();
        // 表单提交
        var parent_id = $(this).attr('id');
        form.on('submit(comment)', function (data) {
            data.field['parent'] = parent_id;
            data.field['article'] = $('#article_id').attr('article_id');
            data.field.info = layedit.getContent(index);

            comment_commit(data.field);
           window.location.reload();
        });

    });
    // 文章评论
    $('#comment-on').click(function () {
        var index = layer.open({
            title: '评论',
            type: 1,
            area: ['1000px', '500px'],
            content: $('#comment-form')
        });
        // layui富文本编辑器创建
        layedit_build();

        // 表单提交
        form.on('submit(comment)', function (data) {
            data.field['article'] = $('#article_id').attr('article_id');
            data.field.info = layedit.getContent(index);
            comment_commit(data.field);
            // layer.close(index);
            // return false;
           window.location.reload();

        })
    });

    // 提交评论内容
    function comment_commit(formdata) {
        console.log(JSON.stringify(formdata));
        $.ajax({
            url: '/blog/comment',
            type: 'POST',
            data: formdata,
            success: function (data) {
                if (data.code === 200) {
                    layer.msg('评论成功!');
                    console.log(data);

                } else {
                    layer.msg('评论失败');
                    console.log(data);
                }
            }
        })
    }

    // layui富文本编辑器创建, 注意:当编辑器放在弹出层时,需要先弹出,再构建编辑器,否则报错失效
    function layedit_build() {
        index = layedit.build('layui-edit', {
            tool: [
                'face', //表情
                'strong' //加粗
                , 'italic' //斜体
                , 'underline' //下划线
                , 'del' //删除线

                , '|' //分割线

                , 'left' //左对齐
                , 'center' //居中对齐
                , 'right' //右对齐
                , 'link' //超链接
                , 'unlink' //清除链接

                // , 'image' //插入图片
                , 'help' //帮助
            ]
        });
    }
});
