from django.shortcuts import render
from django.http import HttpResponse


def test_view(request):
    return render(request, 'test_xhr.html')


def test_xhr_get(request):
    return render(request, 'test_xhr_get.html')


def test_xhr_get_server(request):
    return HttpResponse('This is Ajax')


def reg_view(request):
    return render(request, 'reg.html')


def judge_username(request):
    if request.method == 'GET':
        uname = request.GET['uname']
        if uname == 'stranger':
            return HttpResponse('用户名已存在')
        return HttpResponse('用户名可用%s' % uname)
    elif request.method == 'POST':
        uname = request.POST['uname']
        return HttpResponse('注册成功%s' % uname)

