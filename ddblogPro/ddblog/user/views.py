from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
import json


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
        json_obj = json.loads(json_str.decode())
        username = json_obj['username']
        email = json_obj['email']
        phone = json_obj['phone']
        password_1 = json_obj['password_1']
        password_2 = json_obj['password_2']

        # TODO 参数检查
        if len(username) > 10:
            res = {'code': 10100, 'error': 'The username is wrong'}
            return JsonResponse(res)

        return JsonResponse({'code': 200})
        # return HttpResponse('{"data":"ok"}', content_type='application/json')
