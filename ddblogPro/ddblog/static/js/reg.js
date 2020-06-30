var btn = $('#btn');
var un = $('#username');
var pd = $('#password');
var spd = $('#sure_pd');

btn.on('click', function () {
    if (!un.val()) {
        alert('用户名不能为空')
    } else if (!pd.val()) {
        alert('密码不能为空')
    }else if (!spd.val()){
         alert('请确认密码')
    } else if (pd.val() == spd.val()) {
        $('.login').action = '/user/login';

    }else {
        alert('两次密码不同')
    }
})