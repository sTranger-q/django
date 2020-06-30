from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View


# Create your views here.


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
        return JsonResponse({'data': 'ok'})
        # return HttpResponse('{"data":"ok"}')
