import json
import jieba

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.db.models import F
import os
import time
import hashlib
from .models import *
from django_redis import get_redis_connection
from utils.logging_dec import logging_check2
import paramiko  # 用于调用scp命令
from scp import SCPClient
import shutil

r_search = get_redis_connection('search')


# Create your views here.
def main(request):
    # 添加章节
    if request.method == "GET":
        return render(request, 'book/main.html')


def rename(request):
    # 更改文件夹名字
    return None


def new(request):
    # 创建一本新的漫画
    if request.method == 'GET':
        return render(request, 'book/new.html')
    if request.method == 'POST':
        try:
            book_name = request.POST['book_name']
            book_writer = request.POST['book_writer']
            book_classify = request.POST['book_classify']
        except Exception as e:
            print(e)
            return HttpResponse('提交数据错误，请仔细检查')
        # 将标签转换为对应的二进制数
        count, classify_by = len(book_classify), 0
        for i in range(count):
            classify_by += int(book_classify[i]) * 2 ** (count - i - 1)

        # 在主表创建该图书数据
        book = ComicBook.objects.create(name=book_name, writer=book_writer, classify=classify_by, all_number=0)
        book_id = book.id
        # 在从表创建该图书数据
        ComicPath.objects.create(id_id=book_id, all_number=0)
        # 创建该书文件夹
        os.mkdir(f'{settings.BASE_DIR}/book/static/book/img/{book_id}')
        os.mkdir(f'{settings.BASE_DIR}/book/static/book/img/{book_id}/open')
        os.mkdir(f'{settings.BASE_DIR}/book/static/book/img/{book_id}/vip')
        os.mkdir(f'{settings.BASE_DIR}/book/static/book/img/{book_id}/{book_id}')

        for words in jieba.lcut_for_search(book.name):
            print('取出词语存入redis', words)
            try:
                r_search.sadd(f'{words}', book.id)
            except Exception as e:
                print('错误：', e)

        return render(request, 'book/main.html')


def book(request):
    """
    创建新的漫画时的提示信息
    """
    try:
        book_name = json.loads(request.body)['name']
    except Exception as e:
        print('______________________:', e)
        return JsonResponse({'code': 10020, 'result': '数据错误'})
    try:
        bok = ComicBook.objects.get(name=book_name)
    except Exception:
        return JsonResponse({'code': 200, 'result': 'ok'})
    return JsonResponse(
        {'code': 10021, 'result': f'已有书名：{book_name},ID：{bok.id},作者：{bok.writer},总章节数：{bok.all_number}'})


def chapter_id(request):
    """
    添加漫画章节时的提示信息
    """
    try:
        book_id = json.loads(request.body)['id']
    except Exception as e:
        print('______________________:', e)
        return JsonResponse({'code': 10020, 'result': '数据错误'})
    try:
        bok = ComicBook.objects.get(id=book_id)
    except Exception:
        return JsonResponse({'code': 10022, 'result': '找不到这本书'})
    return JsonResponse(
        {'code': 200, 'result': f'已有书名：{bok.name},ID：{bok.id},作者：{bok.writer},总章节数：{bok.all_number}'})


def chapter_name(request):
    """
    添加漫画章节时的提示信息
    """
    try:
        book_name = json.loads(request.body)['name']
    except Exception as e:
        print('______________________:', e)
        return JsonResponse({'code': 10020, 'result': '数据错误'})
    try:
        bok = ComicBook.objects.get(name=book_name)
    except Exception:
        return JsonResponse({'code': 10022, 'result': '找不到这本书'})
    return JsonResponse(
        {'code': 200, 'result': f'已有书名：{bok.name},ID：{bok.id},作者：{bok.writer},总章节数：{bok.all_number}'})


def ceshi(request):
    return JsonResponse({'code': 200, 'message': f'{ComicBook.objects.filter(id=30)}'})


def jieba_book(request):
    print('函数进入')
    for book in ComicBook.objects.all():
        print(f'{book}', '进入结巴分词')
        for words in jieba.lcut_for_search(book.name):
            print('取出词语存入redis', words)
            try:
                r_search.sadd(f'{words}', book.id)
            except Exception as e:
                print('错误：', e)
            print('存入结束')
    return JsonResponse({'code': 200})


@logging_check2
def add_cathpter(request):
    print('进入添加章节')
    try:
        if request.myuser.user_Name != 'mth123':
            return JsonResponse({'code': 10050, 'error': '非法入侵'})
        print('认证通过')
    except Exception as e:
        print('===========', e)

    json_obj = json.loads(request.body)
    try:
        book_id = json_obj['id']
        begin = json_obj['begin']
        end = json_obj['end']
    except Exception as e:
        print(e)
        return HttpResponse('输入错误')
    print(book_id, begin, end)

    try:
        base_dir = os.path.abspath('../2')
        print(base_dir)
        for file in os.listdir(base_dir):
            shutil.move(f'/{base_dir}/{file}', f'{settings.BASE_DIR}/book/static/book/img/{book_id}/open')
    except Exception as e:
        print('==============', e)
    print('图片移动完成')
    print('开始图片改名')
    md5 = hashlib.md5()
    path = f'{settings.BASE_DIR}/book/static/book/img/{book_id}/open'
    for chapterID in range(int(begin), int(end) + 1):
        try:
            list_book = os.listdir(f'{path}/{chapterID}')
            list_book.sort(key=lambda x: int(x.split('.')[0]))
        except FileNotFoundError:
            return HttpResponse('图片文件未上传')
        for index, img in enumerate(list_book):
            try:
                new_id = int(book_id) << 24 | chapterID << 8 | index + 1
            except Exception as e:
                print(e)
                return HttpResponse('服务器文件夹设置错误')
            md5.update(f'{time.time()}{book_id}{chapterID}{img}'.encode())
            new_name = f'{md5.hexdigest()}'
            # 图片入库 和改名
            try:
                PictureName.objects.create(pictureID=new_id, picture_name=new_name)
            except Exception as e:
                print(e)
                return HttpResponse(f'{index}图片插入数据库失败{book_id}/{chapterID}/{new_name}')
            os.rename(f'{path}/{chapterID}/{img}', f'{path}/{chapterID}/{new_name}.jpg')

        # 章节上传完成，更新总章节数
        ComicBook.objects.filter(id=book_id).update(all_number=F('all_number') + 1)
        ComicPath.objects.filter(id=book_id).update(all_number=F('all_number') + 1)
    print('图片改名完成，mysql同步完成')
    print('开始')
    # 将图片转存入图片服务器
    ssh_up(begin, book_id, end)
    print('图片转移至图床完成')

    return JsonResponse({'code': 200})


def ssh_up(begin, book_id, end):
    """
    将主服务器的图片同步到图床
    :param begin: 开始章节
    :param book_id: 漫画ID
    :param end: 结束章节
    """
    host = settings.SSH_HOST  # 服务器ip地址
    port = 22  # 端口号
    username = settings.SSH_USERNAME  # ssh 用户名
    password = settings.SSH_PASSWORD  # 密码
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh_client.connect(host, port, username, password)
    stdin, stdout, stderr = ssh_client.exec_command(
        f'mkdir -p /home/ubuntu/comic_mlgm_static/static/book/img/{book_id}/open')
    scpclient = SCPClient(ssh_client.get_transport(), socket_timeout=15.0)
    try:
        for i in range(int(begin), int(end) + 1):
            print(f'以上传{i}个章节')
            scpclient.put(f'{settings.BASE_DIR}/book/static/book/img/{book_id}/open/{i}',
                          f'/home/ubuntu/comic_mlgm_static/static/book/img/{book_id}/open', recursive=True)
    except FileNotFoundError as e:
        print(e)
        print("系统找不到指定文件")
    else:
        print("文件上传成功")
    ssh_client.close()


@logging_check2
def new_book(request):
    """
    添加新的漫画
    """
    print('进入添加漫画')
    try:
        if request.myuser.user_Name != 'mth123':
            return JsonResponse({'code': 10050, 'error': '非法入侵'})
        print('认证通过')
    except Exception as e:
        print('===========', e)

    json_obj = json.loads(request.body)
    try:
        book_name = json_obj['book_name']
        book_writer = json_obj['book_writer']
        book_classify = json_obj['book_classify']
    except Exception as e:
        print(e)
        return HttpResponse('提交数据错误，请仔细检查')
    # 将标签转换为对应的二进制数
    count, classify_by = len(book_classify), 0
    for i in range(count):
        classify_by += int(book_classify[i]) * 2 ** (count - i - 1)

    # 在主表创建该图书数据
    book = ComicBook.objects.create(name=book_name, writer=book_writer, classify=classify_by, all_number=0)
    book_id = book.id
    # 在从表创建该图书数据
    ComicPath.objects.create(id_id=book_id, all_number=0)
    # 创建该书文件夹
    os.mkdir(f'{settings.BASE_DIR}/book/static/book/img/{book_id}')
    os.mkdir(f'{settings.BASE_DIR}/book/static/book/img/{book_id}/open')
    os.mkdir(f'{settings.BASE_DIR}/book/static/book/img/{book_id}/vip')
    os.mkdir(f'{settings.BASE_DIR}/book/static/book/img/{book_id}/{book_id}')

    for words in jieba.lcut_for_search(book.name):
        print('取出词语存入redis', words)
        try:
            r_search.sadd(f'{words}', book.id)
        except Exception as e:
            print('错误：', e)
    print('存入结束')

    return JsonResponse({'code': 200})
