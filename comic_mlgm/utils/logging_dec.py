"""
    验证token
"""
import jwt
from django.http import JsonResponse
from django.conf import settings
from user.models import Users


def logging_check(func):
    def wrapper(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            result = {'code': 403, 'error': 'Please login'}
            return JsonResponse(result)

        try:
            res = jwt.decode(token, settings.JWT_TOKEN_KEY, algorithms='HS256')
            print(res)
        except Exception as e:
            print('jwt decode error is %s' % (e))
            result = {'code': 403, 'error': 'Please login'}
            return JsonResponse(result)

        username = res['username']
        user = Users.objects.get(user_Name=username)
        request.myuser = user

        return func(self, request, *args, **kwargs)
    return wrapper


def logging(func):
    """
    验证token但是不会抛出错误，允许非登陆状态使用的装饰器
    """

    def wrapper(request, *args, **kwargs):

        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            print('============没有token')
            return func(request, *args, **kwargs)

        try:
            res = jwt.decode(token, settings.JWT_TOKEN_KEY, algorithms='HS256')
        except Exception as e:
            print('================验证失败')
            return func(request, *args, **kwargs)
        print('=================:token正常通过')
        username = res['username']
        user = Users.objects.get(user_Name=username)
        request.myuser = user
        return func(request, *args, **kwargs)

    return wrapper



def logging_check2(func):
    """
    非 类 的装饰器
    """
    def wrapper(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            result = {'code': 403, 'error': 'Please login'}
            return JsonResponse(result)

        try:
            res = jwt.decode(token, settings.JWT_TOKEN_KEY, algorithms='HS256')
            print(res)
        except Exception as e:
            print('jwt decode error is %s' % (e))
            result = {'code': 403, 'error': 'Please login'}
            return JsonResponse(result)

        username = res['username']
        user = Users.objects.get(user_Name=username)
        request.myuser = user

        return func(request, *args, **kwargs)
    return wrapper