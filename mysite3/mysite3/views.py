from django.shortcuts import render
from django.http import HttpResponse


def test_static(request):
    return render(request, 'test_static.html')


def test_set_cookies(request):
    res = HttpResponse('test set cookies ok')
    res.set_cookie('uuname', 'guoxiaonao', 600)
    return res
