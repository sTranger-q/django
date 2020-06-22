from django.http import HttpResponse
from django.shortcuts import render
import redis
from .models import User

r = redis.Redis(host='127.0.0.1', port=6379, db=0, password='z03104299')


# Create your views here.
def detail_view(request, user_id):
    """
    个人详情页
    :param request:
    :param user_id:
    :return:
    """
    # 先查缓存
    cache_key = 'user:%s' % user_id
    if r.exists(cache_key):
        # 有数据
        data = r.hgetall(cache_key)
        # {b'username':b'xxxx',b'age':b'xxx'}--->普通字符字典
        new_data = {k.decode(): v.decode() for k, v in data.items()}
        username = new_data['username']
        age = new_data['age']
        html = 'username id %s age is %s ' % (username, age)
        return HttpResponse(
            'cache: username is %s age is %s ' % (username, age))
    # 没有缓存
    try:
        user = User.objects.get(id=user_id)
    except Exception as e:
        return HttpResponse('none')
    age = user.age
    username = user.username
    html = 'username is %s age is %s ' % (username, age)
    # 更新缓存
    r.hmset(cache_key, {'username': username, 'age': age})
    r.expire(cache_key, 30)
    return HttpResponse(html)


def update_view(request, user_id):
    # /user/update/1?age=30
    new_age = request.GET['age']
    # 查->改->存
    user = User.objects.get(id=user_id)
    user.age = new_age
    user.save()

    # 删缓存,存不存在都不会报错
    cache_key = 'user:%s' % user_id
    r.delete(cache_key)
    return HttpResponse('----update success----')
