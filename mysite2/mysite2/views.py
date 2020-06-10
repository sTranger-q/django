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
    dict01['age'] = 18
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
