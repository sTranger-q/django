var btn = $('#btn');
var un = $('#username');
var pd = $('#password');


btn.on('click', function () {
    if (!un.val()) {
        pd.val('')
        alert('用户名不能为空')
    } else if (!pd.val()) {
        un.val('')
        alert('密码不能为空')
    } else {
        $('.login').action = '/user/login';

    }
})