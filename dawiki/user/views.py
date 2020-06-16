from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import *
import hashlib


# Create your views here.
def login_view(request):
    if request.method == 'GET':
        # 判断session
        # uname = request.session.get('username')
        # if not uname:
        #     # 判断Cookies
        #     uname = request.COOKIES.get('username')
        #     if not uname:
        #         return render(request, 'user/login.html')
        #     request.session['username'] = uname
        # return HttpResponseRedirect('/')
        if 'username' in request.session and 'uid' in request.session:
            return HttpResponseRedirect('/')
        username = request.COOKIES.get('username')
        uid = request.COOKIES.get('uid')
        if username and uid:
            request.session['username'] = username
            request.session['uid'] = uid
            return HttpResponseRedirect('/')
        return render(request, 'user/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        pd_in = request.POST.get('password')
        if not username or not pd_in:
            return HttpResponseRedirect('/user/login')
        try:
            old_user = User.objects.get(username=username)


        except Exception as e:
            return HttpResponseRedirect('/user/login')
        p = hashlib.md5()
        p.update(pd_in.encode())
        if p.hexdigest() == old_user.password:
            request.session['uid'] = old_user.id
            request.session['username'] = username
            res = HttpResponse('login successfully')
            if 'remember' in request.POST:
                res.set_cookie('uid', old_user.id, 3600 * 24 * 3)
                res.set_cookie('username', username, 3600 * 24 * 3)
            return res
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
                new_user = User.objects.create(username=un, password=password_h)

                # 免登录一天
                request.session['username'] = new_user.username
                request.session['uid'] = new_user.id

                return HttpResponse('注册成功')
            except Exception as e:
                return HttpResponse('The username is already existed')


def logout_view(request):
    if 'username' in request.session:
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']
    response = HttpResponseRedirect('/')
    if 'username' in request.COOKIES:
        response.delete_cookie('username')
    if 'uid' in request.COOKIES:
        response.delete_cookie('uid')
    return response
