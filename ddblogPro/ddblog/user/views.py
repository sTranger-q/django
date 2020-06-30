from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
import json
from .models import UserProfile
import hashlib


# Create your views here.

# 异常状态码: 10100-10199


# FBV f:function
def users_view(request):
    return HttpResponse('--user view')


# CBV C:class 内部解耦
class UserView(View):
    # 方法名同method名
    def get(self, request):
        return HttpResponse('--CBV get view')

    def post(self, request):
        print('----POST comming')
        # <QueryDict: {}>  POST-->针对与表单提交
        # print(request.POST)

        json_str = request.body  # 请求体内
        # print(11111111)
        # b'{"username":"stranger".....}'
        # print(json_str)
        # 取数据
        json_obj = json.loads(json_str)
        username = json_obj['username']
        email = json_obj['email']
        phone = json_obj['phone']
        password_1 = json_obj['password_1']
        password_2 = json_obj['password_2']
        # TODO 参数检查
        if len(username) > 13:
            res = {'code': 10100, 'error': 'The username is wrong'}
            return JsonResponse(res)
        if password_1 != password_2:
            res = {'code': 10101, 'error': 'two password different'}
            return JsonResponse(res)
        old_user = UserProfile.objects.filter(username=username)
        if old_user:
            res = {'code': 10102, 'error': 'username existed'}
            return JsonResponse(res)
        # hash加密密码
        m = hashlib.md5()
        m.update(password_1.encode())
        password_h = m.hexdigest()
        try:
            UserProfile.objects.create(username=username,
                                       nickname=username,
                                       email=email,
                                       password=password_h, phone=phone)
        except Exception as e:
            print('----create error----')
            print(e)
            res = {'code': 10103, 'error': 'register is defeated'}
            return JsonResponse(res)
        # jwt
        return JsonResponse({'code': 200})
        # return HttpResponse('{"data":"ok"}', content_type='application/json')
