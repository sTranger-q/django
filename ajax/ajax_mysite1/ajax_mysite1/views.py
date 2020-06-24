from django.shortcuts import render
from django.http import HttpResponse


def test_view(request):
    return render(request, 'test_xhr.html')


def test_xhr_get(request):
    return render(request, 'test_xhr_get.html')


def test_xhr_get_server(request):
    return HttpResponse('This is Ajax')
