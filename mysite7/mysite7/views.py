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