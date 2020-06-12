var arr = ['0', '1', '2', '4', '7', '6', '5', '3'];
var img = document.getElementsByClassName('luck');
var btn = document.getElementById('btn');
var i = 0
img[0].className = 'luck gre';
btn.onclick = function () {
    var kp = (Math.floor(Math.random() * 5) + 5) * 1000;
    console.log(kp);
    var timer1 = setInterval(draw, 100)
    var timer2 = setTimeout(function () {
        clearInterval(timer1);
        $('.gre').addClass('fun')
        var timer3 = setInterval(fun, 100)
        var timer4 = setTimeout(function () {
            $('.fun').addClass('gre');
            clearInterval(timer3);
        }, 2000)
    }, kp);
}

function fun() {
    $('.fun').toggleClass('gre');
}

function draw() {

    img[arr[i]].className = 'luck';

    if (i == arr.length - 1) {
        i = 0;
    } else {
        i += 1;
    }
    img[arr[i]].className = 'luck gre';

}