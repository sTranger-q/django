from django.shortcuts import render
from django.http import HttpResponse


def test_static(request):
    return render(request, 'test_static.html')


def test_set_cookies(request):
    res = HttpResponse('test set cookies ok')
    res.set_cookie('uuname', 'guoxiaonao', 600)
    return res


def test_get_cookies(request):
    value = request.COOKIES.get('uuname', 'no')
    print('=============')
    print(value)
    print('=============')
    return HttpResponse('uuname:' + value)


def set_sessions(request):
    request.session['name'] = 'stranger'
    return HttpResponse('set session is ok')


def get_sessions(request):
    return HttpResponse('session name is %s' % request.session['name'])
