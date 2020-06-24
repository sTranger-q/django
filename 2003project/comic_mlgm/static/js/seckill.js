$('#ssss').ready(function () {
    $('.noStart01')[0].style.display = 'block';
    $('.noStart02')[0].style.display = 'none';
    $('.noStart03')[0].style.display = 'none';
    $.ajax({
        type: "GET",
        url: "/seckill/time",
        headers: {
            'Authorization': window.localStorage.token
        },
        dataType: 'json',
        success: function (res) {
            if (res.code == 200) {
                var time01 = res.timeout;
                var time02 = res.continue_time;
                console.log(time01);
                var timer = setInterval(function () {
                    // var time = new Date();
                    if (time01 > 0) {
                        $('.noStart01')[0].style.display = 'none';
                        $('.noStart02')[0].style.display = 'block';
                        $('.noStart03')[0].style.display = 'none';
                        var hours = parseInt(time01 / 3600);
                        var minute = parseInt((time01 % 3600) / 60);
                        var second = parseInt((time01 % 3600) % 60);
                        $('.Hours').html(hours);
                        $('.Min').html(minute);
                        $('.Second').html(second);
                        time01--;
                    } else {
                        $('.noStart01')[0].style.display = 'none';
                        $('.noStart02')[0].style.display = 'none';
                        $('.noStart03')[0].style.display = 'block';
                        $('#secskill').click(function () {
                            $.ajax({
                                url: '/seckill',
                                type: 'GET',
                                headers: {
                                    'Authorization': window.localStorage.token
                                },
                                dataType: 'json',
                                success: function (result) {
                                    if (result.code == 200) {
                                        window.location = result.url
                                    } else {
                                        alert(result.error)
                                    }
                                }
                            })
                        });
                        console.log(time02);
                        // var time = new Date();
                        var hours = parseInt(time02 / 3600);
                        var minute = parseInt((time02 % 3600) / 60);
                        var second = parseInt((time02 % 3600) % 60);
                        $('.Hours').html(hours);
                        $('.Min').html(minute);
                        $('.Second').html(second);
                        time02--;
                    }
                    if (time02 < 0) {
                        $('.noStart01')[0].style.display = 'block';
                        $('.noStart02')[0].style.display = 'none';
                        $('.noStart03')[0].style.display = 'none';
                        $('#secskill').remove();
                        clearInterval(timer)
                    }
                }, 1000);
            } else {
                $('.noStart01')[0].style.display = 'block';
                $('.noStart02')[0].style.display = 'none';
                $('.noStart03')[0].style.display = 'none';
            }
        },
    })
})