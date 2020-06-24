import math
from typing import List
import jieba
import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.core.cache import cache
from django_redis import get_redis_connection
from redis import Redis
from django.conf import settings

from book.models import *
from utils.logging_dec import logging

# Create your views here.

r = get_redis_connection('default')  # type:Redis
r_search = get_redis_connection('search')


def index(request):
    return render(request, 'index.html')


def details(request):
    try:
        id = request.GET['id']
    except Exception as e:
        print(e)
        return HttpResponse('no')
    return render(request, 'details.html', {'id': id})


@logging
def picture(request):
    """
    首页图片展示
    """
    try:
        classify_list = r.lrange(f'classify_{request.myuser.id}', 0, -1)
    except Exception as e:
        print('未登录状态')
        return JsonResponse(
            [{'name': book.name, 'path': f'http://49.233.38.13/static/book/img/{book.id}/{book.id}/0.jpg',
              'id': book.id} for book in
             ComicBook.objects.filter(is_active=True)][:18], safe=False)
    if not classify_list:
        print('===========request.myuser.id没找到')
        return JsonResponse(
            [{'name': book.name, 'path': f'http://49.233.38.13/static/book/img/{book.id}/{book.id}/0.jpg',
              'id': book.id} for book in
             ComicBook.objects.filter(is_active=True)][:18], safe=False)
    user_classify_list = [0 for __ in range(settings.COMIC_LABEL_COUNT)]
    for number in classify_list:
        for i in range(settings.COMIC_LABEL_COUNT):
            if int(number.decode()) & (1 << i):
                user_classify_list[settings.COMIC_LABEL_COUNT - 1 - i] += 1
    cosine_dict = {book.id: cosine(user_classify_list,
                                   [book.classify & (1 << i) for i in range(settings.COMIC_LABEL_COUNT - 1, -1, -1)])
                   for book in ComicBook.objects.filter(is_active=True)}
    list01 = [{'name': ComicBook.objects.get(id=book_id).name,
               'path': f'http://49.233.38.13/static/book/img/{book_id}/{book_id}/0.jpg',
               'id': book_id}
              for book_id in sorted(cosine_dict, key=lambda k: cosine_dict[k], reverse=True)[:18]]
    return JsonResponse(list01, safe=False)


def cosine(a: List[int], b: List[int]):
    """
    计算用户和漫画的相似度
    :param a: 用户喜好向量
    :param b: 漫画标签向量
    :return: cosine值(0~1)(值越大，相似度越高)
    """
    len_a = len(a)
    if len_a == len(b):
        a_dian_b = a_mo = b_mo = 0
        for i in range(len_a):
            a_dian_b += a[i] * b[i]
            a_mo += a[i] ** 2
            b_mo += b[i] ** 2
        a_mo_b_mo = math.sqrt(a_mo) * math.sqrt(b_mo)
        return a_dian_b / a_mo_b_mo
    else:
        raise ('用户向量和漫画向量长度不等')


def details_id(request, x):
    """
    漫画章节展示
    :param x: 漫画ID
    """
    count = 1
    list01 = []
    try:
        open_name = ComicPath.objects.get(id_id=x).open_name
    except Exception as e:
        print('______________:', e)
        return JsonResponse({'code': 10002, 'error': '找不到了个喵'})
    while True:
        pictureID = x << 24 | count << 8 | 1
        purl = cache.get(f'purl:{pictureID}')
        if not purl:
            try:
                picture_name = PictureName.objects.get(pictureID=pictureID).picture_name
            except Exception:
                return JsonResponse(list01, safe=False)
            purll = f'http://49.233.38.13/static/book/img/{x}/{open_name}/{count}/{picture_name}.jpg'
            cache.set(f'purl:{pictureID}', purll, 3600)
            list01.append({'chapter': count, 'path': purll})
        else:
            list01.append({'chapter': count, 'path': purl})
        count += 1


def contents(request, x, y):
    return render(request, 'contents.html', {'book_id': x, 'chapter_id': y})


@logging
def content(request, x, y, z):
    """
    漫画观看页面

    将三个参数计算出主键之后去数据库中查找对应的图片地址（优先redis），如果找不到，说明该章节结束，把章节ID + 1，页数重置为1，再次查找，如果还是找不到，说明正本漫画结束
    返回给客户端的数据除了请求图片的地址，还包含了客户端下次发起请求应该携带的参数

    :param x: 漫画ID
    :param y: 章节ID
    :param z: 页数ID
    """
    try:
        open_name = ComicPath.objects.get(id_id=x).open_name
    except Exception as e:
        print('_________________1:', e)
        return JsonResponse({'url': '', 'code': 10003})
    pictureID = x << 24 | y << 8 | z
    purl = cache.get(f'purl:{pictureID}')
    if purl: return JsonResponse({'url': purl, 'book_id': x, 'chapter_id': y, 'page_id': z + 1})
    try:
        picture_name = PictureName.objects.get(pictureID=pictureID).picture_name
    except Exception:
        y += 1
        z = 1
        pictureID_2 = x << 24 | y << 8 | z
        purl2 = cache.get(f'purl:{pictureID}')
        if purl2: return JsonResponse({'url': purl2, 'book_id': x, 'chapter_id': y, 'page_id': z + 1})
        try:
            picture_name = PictureName.objects.get(pictureID=pictureID_2).picture_name
        except Exception as e:
            print('__________________3:', e)
            return JsonResponse({'url': '', 'code': 10003})
        # 每看到下一章，将该漫画的标签存入用户的喜好中
        try:
            weighting(request.myuser.id, x)
        except Exception as e:
            print(e)
        purl2l = f'http://49.233.38.13/static/book/img/{x}/{open_name}/{y}/{picture_name}.jpg'
        cache.set(f'purl:{pictureID}', purl2l, 3600)
        return JsonResponse({'url': purl2l, 'book_id': x, 'chapter_id': y, 'page_id': z + 1})
    purll = f'http://49.233.38.13/static/book/img/{x}/{open_name}/{y}/{picture_name}.jpg'
    cache.set(f'purl:{pictureID}', purll, 3600)
    return JsonResponse({'url': purll, 'book_id': x, 'chapter_id': y, 'page_id': z + 1})


def weighting(userid, book_id):
    """
    将漫画标签存入用户喜好
    :param userid: 用户ID
    :param book_id: 漫画ID
    """
    if r.llen(f'classify_{userid}') == 20:
        r.lpop(f'classify_{userid}')
        r.rpush(f'classify_{userid}', ComicBook.objects.get(id=book_id).classify)
    else:
        r.rpush(f'classify_{userid}', ComicBook.objects.get(id=book_id).classify)

    print('===========兴趣爱好已存入')


def screen(request, x):
    list01 = [
        {'name': book.name, 'path': f'http://49.233.38.13/static/book/img/{book.id}/{book.id}/0.jpg', 'id': book.id} for
        book in
        ComicBook.objects.filter(is_active=True) if book.classify & x]
    return JsonResponse(list01, safe=False)


def search(request):

    json_obj = json.loads(request.body.decode())
    words = json_obj['words']
    print(words)
    bookid_set = r_search.smembers(words)
    print(bookid_set)
    if bookid_set:
        book = ComicBook.objects.get(id=int(list(bookid_set)[0].decode()))
        if book.is_active:
            return JsonResponse([{'code': 200, 'name': book.name, 'id': book.id,
                                  'path': f'http://49.233.38.13/static/book/img/{book.id}/{book.id}/0.jpg'}],
                                safe=False)
        return JsonResponse({'code': 10041, 'error': '该书已下嫁了个喵'})

    list01 = jieba.lcut(words)
    list01.sort(key=lambda i: len(i), reverse=True)
    dict01 = {}
    for word in list01:
        for id in r_search.smembers(word):
            if id in dict01:
                dict01[id] = dict01[id] + 1
            else:
                dict01[id] = 1
    list02 = sorted(dict01, key=lambda i: dict01[i], reverse=True)
    list03 = []
    for id in list02:
        book = ComicBook.objects.get(id=int(id.decode()))
        if book.is_active:
            list03.append({'code': 200, 'name': book.name, 'id': book.id,
                           'path': f'http://49.233.38.13/static/book/img/{book.id}/{book.id}/0.jpg'})
    return JsonResponse(list03, safe=False)
