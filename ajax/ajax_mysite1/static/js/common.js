function createXhr() {
    if (window.XMLHttpRequest) {
        var xhr = new XMLHttpRequest();

    } else {
        var xhr = new ActiveXObject('Microsoft.XMLHTTP');
    }
    return xhr;
}

function getXhr() {
    var xhr = createXhr();
    xhr.open('GET', '/test_xhr_get_server', true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var div = document.getElementById('show');
            div.innerHTML = xhr.responseText;
            // 增加计时器，限制按钮点击次数
        }
    }
    xhr.send(null);
}

$(function () {
    $('#uname').blur(function () {
        var xhr = createXhr();
        var url = '/judge_username?uname=' + $('#uname').val();
        xhr.open('GET', url, true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                $('#tip').html(xhr.responseText);
            }
        }
        xhr.send(null);
    })
    $('#btn').click(function () {
        var xhr = createXhr();
        xhr.open('POST', '/judge_username', true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                alert(xhr.responseText)
            }
        }
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        var uname = $('#uname').val();
        var pwd = $('#pwd').val();
        var csrf = $("[name='csrfmiddlewaretoken']").val();
        var params = 'uname=' + uname + '&pwd' + pwd
            + '&csrfmiddlewaretoken=' + csrf;
        xhr.send(params);
    })
})