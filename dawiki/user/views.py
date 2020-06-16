from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import *
import hashlib


# Create your views here.
def login_view(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        pd_in = request.POST.get('password')
        if not username or not pd_in:
            return HttpResponseRedirect('/user/login')
        try:
            pd = User.objects.get(username=username).password
        except Exception as e:
            return HttpResponseRedirect('/user/login')
        if pd_in == pd:
            request.session['username'] = username
            return HttpResponse('login successfully')
        else:
            return HttpResponseRedirect('/user/login')


def reg_view(request):
    if request.method == 'GET':
        return render(request, 'user/reg.html')
    elif request.method == 'POST':
        un = request.POST.get('username')
        pd_1 = request.POST.get('password')
        pd_2 = request.POST.get('sure_pd')
        if not un or not pd_1 or not pd_2:
            return HttpResponseRedirect('/user/reg')
        try:
            User.objects.get(username=un)
            return HttpResponse('The username is already existed')
        except Exception as e:
            # 密码处理
            # hash算法:明文--->hash值
            # 1.算法恒定 定长输出
            m = hashlib.md5()
            m.update(pd_1.encode())
            password_h = m.hexdigest()
            try:
                # 存在高并发问题
                User.objects.create(username=un, password=password_h)

                # 免登录一天
                request.session['username'] = un

                return HttpResponse('注册成功')
            except Exception as e:
                return HttpResponse('The username is already existed')


def logout_view(reques):
    pass
