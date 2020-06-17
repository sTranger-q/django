import csv

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
import time


@cache_page(60)
def test_cache(request):
    # time.sleep(3)
    t1 = time.time()

    return HttpResponse('t1 is %s' % t1)
    # return render(request, 'test_cache.html', locals())


def test_csrf(request):
    if request.method == 'GET':
        return render(request, 'test_csrf.html')
    elif request.method == 'POST':
        return HttpResponse('---post ok')


def test_csv(request):
    response = HttpResponse(content_type='test/csv')
    response['Content-Disposition'] = 'attachment;filename="book.csv"'
    all_book = [{'id': 1, 'title': 'Python1'}, {'id': 2, "title": "Python2"}]
    writer = csv.writer(response)
    writer.writerow(['id', 'title'])
    for book in all_book:
        writer.writerow([book['id'], book['title']])
    return response
