from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render


def test_html(request):
    # 方案1 loader
    # 加载
    # t = loader.get_template('test_html.html')
    # 2.生成html字符串
    # html = t.render()
    # 3.return
    # return HttpResponse(html)

    # 方案2 render
    dict01 = {}
    dict01['str'] = 'zhongjian'
    dict01['int'] = 18
    dict01['lst'] = ['Jack', 'Tom', 'Lily']
    dict01['d'] = {'name': 'guoxiaonao', 'desc': 'haha'}
    dict01['function'] = say_hi
    dict01['obj'] = Dog()
    # script is &lt;script&gt;alert(11)&lt;/script&gt;
    dict01['script'] = '<script>alert(11)</script>'

    return render(request, 'test_html.html', dict01)


def say_hi():
    return 'hahahahahh'


class Dog:

    def say(self):
        return 'wangwang'


def mycal(request):
    # dict01 = {}
    if request.method == "GET":
        x = 1
        op = 'add'
        y = 2
        res = 3
        return render(request, 'cal_test.html', locals())
    if request.method == 'POST':
        try:
            x = int(request.POST['x'])
            op = request.POST['op']
            y = int(request.POST['y'])
        except ValueError:
            return HttpResponse('Please give me number')
        # if not x or not y:
        #     return HttpResponse('Please give me number!!')
        if op == 'add':
            res = x + y
        elif op == 'sub':
            res = x - y
        elif op == 'mul':
            res = x * y
        elif op == 'div':
            if y == 0:
                return HttpResponse("y can't be 0")
            else:
                res = x / y

        return render(request, 'cal_test.html', locals())
