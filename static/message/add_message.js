$(function () {
    $('#submit').click(function () {
        var name = $('#name').val();     //.trim();
        // var address = $('#message input[name="address"]').val().trim();
        var mobile = $('#mobile').val();//.trim();
        // var email = $('#message input[name="email"]').val().trim();
        var content = $('#content').val();//.trim();

        // 姓名判空
        if (name.length < 1) {
            layer.msg('请输入姓名！');
            return false;
        }
        // if (address.length < 1){
        //     layer.msg('请输入正确的地址');
        //     return false;
        // }
        // 电话验证
        var reg_mobile = /^1[3456789]\d{9}$/;
        if (reg_mobile.test(mobile) === false) {
            layer.msg('请输入正确的电话号码！');
            return false;
        }
        // 邮箱验证
        // var reg_email = /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/;
        // if (reg_email.test(email) === false){
        //     layer.msg('请输入正确的邮箱！');
        //     return false;
        // }
        if (content.length < 5) {
            layer.msg('留言内容不得少于5个字！');
            return false
        }
        $.post('/add/message/',
            {
                name: name,
                mobile: mobile,
                // address: address,
                content: content,
                // email: email,
            }, function (data) {
                data = JSON.parse(data);
                console.log(data);
                if (data.code == 0) {
                    layer.msg('留言成功');
                    return false;
                } else {
                    layer.msg('留言失败！')
                }
            })
    });
});