from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect


def index_view(request):
    return render(request, 'index.html')


def page_view(request, page):
    # print(type(page)) # -->int
    if page < 10:
        page = '0%s' % page
    else:
        page = str(page)
    return render(request, 'page%s.html' % page)


def test_view(request):
    return HttpResponseRedirect(reverse('page', args=[1]))
