import base64
import json
import string
import time

from django.conf import settings
from django.core.cache import cache, caches
from django.db import transaction
from django.http import HttpResponse, request, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from utils.logging_dec import logging_check
from .models import *
from .tasks import send_email
import hashlib
import random
import jwt


# Create your views here.


# 注册


def register_view(request):
    # get请求
    return render(request, "user/register.html")


def send_verification_code_view(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    username = json_obj['username']
    email = json_obj['email']
    try:
        # 发送验证码
        send_v_code(username, email)
    except Exception as e:
        print(e)
        return JsonResponse({'code': 10100,
                             'error': 'Sending verification code is defeated!'})
    return JsonResponse({'code': 200})


def send_v_code(username, email):
    # 把验证码存入缓存
    v_code = str(random.randint(100000, 999999))
    v_code_str = '%s_%s' % (username, email)
    cache.set(v_code_str, v_code, 120)

    # 发送邮件验证码
    subject = 'mlgm验证邮件'
    content = '你的验证码是%s,请在120秒内进行验证' % v_code
    send_email.delay(subject, email, content)


def register_server_view(request):
    json_str = request.body

    json_obj = json.loads(json_str)

    username = json_obj['username']
    password_1 = json_obj['password_1']
    password_2 = json_obj['password_2']
    email = json_obj['email']
    v_code = json_obj['v_code']
    # 检查用户名是否可用
    old_users = Users.objects.filter(user_Name=username)
    if old_users:
        result = {'code': 10101, 'error': 'The username is already existed !'}
        return JsonResponse(result)
    # 创建用户 Users创建数据
    # 检查username是否可用
    # 密码处理
    # hash算法
    if password_1 != password_2:
        return JsonResponse({'code': 10102, 'error': "请确认密码相同！"})

    m = hashlib.md5()
    m.update(password_1.encode())
    password_h = m.hexdigest()

    # 对验证码进行验证
    res = verify_v_code(username, email, v_code)
    if res:
        JsonResponse(res)
    else:
        try:
            user = Users.objects.create(user_Name=username, password=password_h, user_Email=email)
        except Exception as e:
            print(e)
            result = {'code': 10105, 'error': '该用户名已存在 !'}
            return JsonResponse(result)

        return JsonResponse({'code': 200})


def verify_v_code(username, email, v_code):
    key = "%s_%s" % (username, email)
    cache_v_code = cache.get(key)
    if not cache_v_code:
        return {'code': 10103, 'error': 'The verification code is expired '}
    else:
        if v_code != cache_v_code:
            return {'code': 10104, 'error': 'The verification code is error!'}
        else:
            return


# 登录


def login_view(request):
    # get请求
    return render(request, "user/login.html")


def login_server_view(request):
    json_str = request.body
    json_obj = json.loads(json_str)

    username = json_obj["username"]
    password = json_obj["password"]

    try:

        old_user = Users.objects.get(user_Name=username)
    except Exception as e:
        print(e)
        return JsonResponse({'code': 10200, 'error': '用户名或密码错误~'})
    m = hashlib.md5()
    m.update(password.encode())
    password_h = m.hexdigest()

    if password_h != old_user.password:
        return JsonResponse({'code': 10201, 'error': '用户名或密码错误~'})
    # 签发token
    token = make_token(username)
    result = {'code': 200, 'username': username, 'data': {'token': token.decode()}}
    return JsonResponse(result)


def make_token(username, expire=3600 * 24):
    now = time.time()
    payload = {'username': username, 'exp': int(now + expire)}
    key = settings.JWT_TOKEN_KEY
    return jwt.encode(payload, key, algorithm='HS256')


# 找回密码
def retrieve_view(request):
    username = request.GET.get('username')
    return render(request, "user/retrieve_passwd.html", locals())


def verify_user_by_email_view(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    username = json_obj['username']
    email = json_obj['email']

    try:
        user = Users.objects.get(user_Name=username)
    except Exception as e:
        print('---verification error is')
        print(e)
        return JsonResponse({'code': 10300, 'error': '该用户不存在'})
    if email == user.user_Email:
        try:
            # 发送验证码
            send_v_code(username, email)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 10302,
                                 'error': 'Sending verification code is defeated!'})
        return JsonResponse({'code': 200})
    else:
        return JsonResponse({'code': 10301, 'error': '邮箱错误!'})


def verify_code_view(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    username = json_obj['username']
    email = json_obj['email']
    v_code = json_obj['v_code']
    # 对验证码进行验证
    res = verify_v_code(username, email, v_code)
    if res:
        return JsonResponse(res)
    else:
        return JsonResponse({'code': 200})


def reset_password_view(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    username = json_obj['username']
    password_1 = json_obj['password_1']
    password_2 = json_obj['password_2']

    try:
        user = Users.objects.get(user_Name=username)
    except Exception as e:
        print('---verification error is')
        print(e)
        return JsonResponse({'code': 10300, 'error': '该用户不存在'})
    # 创建用户 Users创建数据
    # 检查username是否可用
    # 密码处理
    # hash算法
    if password_1 != password_2:
        return JsonResponse({'code': 10304, 'error': "请确认密码相同！"})

    m = hashlib.md5()
    m.update(password_1.encode())
    password_h = m.hexdigest()

    user.password = password_h
    user.save()

    return JsonResponse({"code": 200})

# # 微博第三方登录
# def weibo_login_view(request):
#     # get请求
#     if request == "GET":
#         return render(request, "user/weibo_login.html")
#     # post请求
#     elif request.method == "POST":
#         return HttpResponse("Authorized is ok")





