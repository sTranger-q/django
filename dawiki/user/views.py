import random
from django.core import mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import *
import hashlib
from django.contrib import messages
import redis

Pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=6)
r = redis.Redis(connection_pool=Pool)


def creat_check_number():
    lis = []
    for i in range(6):
        lis.append(str(random.randint(0, 9)))
    return ''.join(lis)


# Create your views here.
def login_view(request):
    """
    登录视图
    :param request:
    :return:
    """
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

        # 如果session中有保存用户名和用户id,则直接跳转主页
        if 'username' in request.session and 'uid' in request.session:
            return HttpResponseRedirect('/')
        # 在cookie中找出username 和 id， 如果存在，则直接跳转主页
        username = request.COOKIES.get('username')
        uid = request.COOKIES.get('uid')
        if username and uid:
            request.session['username'] = username
            request.session['uid'] = uid
            return HttpResponseRedirect('/')
        # 获取验证信息
        msg = request.COOKIES.get('msg', 'right')
        # 如果session和cookie中都没有用户信息，则进入登录界面
        return render(request, 'user/login.html', {'msg': msg})
    elif request.method == 'POST':
        username = request.POST.get('username')
        pd_in = request.POST.get('password')
        # 如果输入为空,刷新页面
        if not username or not pd_in:
            return HttpResponseRedirect('/user/login')
        try:
            # 在数据库中找到用户数据
            old_user = User.objects.get(username=username)
        except Exception as e:
            # 如果不存在username,刷新页面

            messages.error(request, '账号不存在')

            return HttpResponseRedirect('/user/login')
        p = hashlib.md5()
        p.update(pd_in.encode())
        # 判断密码是否正确
        if p.hexdigest() == old_user.password:
            # 将用户信息加入session
            request.session['uid'] = old_user.id
            request.session['username'] = username
            res = HttpResponseRedirect('/')
            # 判断是否勾选记住账户
            if 'remember' in request.POST:
                # 将信息加入cookie
                res.set_cookie('uid', old_user.id, 3600 * 24 * 3)
                res.set_cookie('username', username, 3600 * 24 * 3)
                res.delete_cookie('msg')
            return res
        else:

            messages.error(request, '密码错误')
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
        if pd_1 != pd_2:
            return HttpResponseRedirect('/user/reg')
        try:
            User.objects.get(username=un)
            messages.error(request, '账户已存在1')
            return HttpResponseRedirect('/user/reg')
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
                messages.success(request, '注册成功')
                return HttpResponseRedirect('/')
            except Exception as e:
                messages.error(request, '已存在')
                return HttpResponseRedirect('/user/regredis')


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


def forget_view(request):
    if request.method == 'GET':
        return render(request, 'user/forget.html')
    elif request.method == 'POST':
        email = request.POST.get('mailAddr')
        username = request.POST.get('username')
        if not email or not username:
            messages.error(request, '请输入邮箱/用户名')
            return HttpResponseRedirect('/user/forget')
        try:
            user = User.objects.get(username=username)
        except Exception as e:

            messages.error(request, '用户名不存在:%s' % e)
            return HttpResponseRedirect('/user/forget')
        if user.email == email:
            # 发验证码 待改进
            check_number = creat_check_number()
            key = f'forget:{user.id}'
            r.set(key, check_number, ex=180, nx=True)
            request.session['forget_uid'] = user.id
            mail.send_mail('验证码',
                           check_number,
                           '853561128@qq.com',
                           recipient_list=[email])
            return HttpResponseRedirect('/user/check')
        else:
            messages.error(request, '邮箱错误')
            return HttpResponseRedirect('/user/forget')


def check_view(request):
    if request.method == 'GET':
        return render(request, 'user/check.html')
    elif request.method == 'POST':
        check_input = request.POST['check_number']
        uid = request.session['forget_uid']
        key = f'forget:{uid}'
        check_number = r.get(key).decode()
        if str(check_input) == str(check_number):
            return HttpResponseRedirect('/user/cpd')
        else:
            messages.error(request, '验证码错误')
            return HttpResponseRedirect('/user/forget')


def cpd_view(request):
    if request.method == 'GET':
        return render(request, 'user/cpd.html')
    elif request.method == 'POST':
        pd1 = request.POST['password']
        pd2 = request.POST['sure_pd']
        if pd1 != pd2:
            messages.error(request, '两次输入密码不同')
            return HttpResponseRedirect('user/cpd')
        uid = request.session['forget_uid']
        user = User.objects.get(id=uid)
        # 密码处理
        # hash算法:明文--->hash值
        # 1.算法恒定 定长输出
        m = hashlib.md5()
        m.update(pd1.encode())
        password_h = m.hexdigest()
        user.password = password_h
        user.save()

        # 处理session
        del request.session['forget_uid']
        request.session['username'] = user.username
        request.session['uid'] = user.id
        messages.success(request, '注册成功')
        return HttpResponseRedirect('/')
