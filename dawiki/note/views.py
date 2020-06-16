from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import *


# 装饰器
def logging_check(fn):
    def wrapper(request, *args, **kwargs):
        # 检查session
        if 'username' not in request.session or 'uid' not in request.session:
            # 检查cookies[回写]
            if 'username' not in request.COOKIES or 'uid' not in \
                    request.COOKIES:
                return HttpResponseRedirect('/user/login')
            else:
                request.session['username'] = request.COOKIES.get('username')
                request.session['uid'] = request.COOKIES.get('uid')

        # 如果未登录，return 302 -> login
        return fn(request, *args, **kwargs)

    return wrapper


# Create your views here.
@logging_check
def list_view(request):
    if request.method == 'GET':
        username = request.session['username']
        uid = request.session['uid']
        notes = Note.objects.filter(user_id=uid)

        return render(request, 'note/list_note.html', locals())


@logging_check
def add_view(request):
    if request.method == 'GET':
        return render(request, 'note/add_note.html')
    elif request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        # 获取登录用户id
        uid = request.session['uid']
        # 存
        Note.objects.create(title=title, content=content, user_id=uid)
        return HttpResponseRedirect('/note')


@logging_check
def mod_view(request, nid):
    if request.method == 'GET':
        username = request.session['username']
        note = Note.objects.get(id=nid)
        return render(request, 'note/mod_note.html', locals())
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if not title or not content:
            return HttpResponseRedirect('/note/mod/%s' % nid)
        try:
            note = Note.objects.get(id=nid)
            note.title = title
            note.content = content
            note.save()
        except Exception as e:
            return HttpResponse('出错啦')
        return HttpResponseRedirect('/note')


@logging_check
def del_view(request, nid):
    try:
        note = Note.objects.get(id=nid)
        note.delete()
    except Exception as e:
        return HttpResponse('删除失败')
    return HttpResponseRedirect('/note')
