from django.http import HttpResponse, HttpResponseRedirect

POST_FORM = """
<form method='post' action="/test_get_post">
    姓名:<input type="text" name="username">
    <input type='submit' value='登陆'>
</form>

"""


def page_2003_view(request):
    return HttpResponse('这是page2003页面')


def index_view(request):
    return HttpResponse('这是首页')


def page1_view(request):
    return HttpResponse('这是page1')


def page2_view(request):
    return HttpResponse('这是page2')


def page_view(request, page):
    return HttpResponse('这是page%d!!!!' % page)


def calculator_view(request, num1, sign, num2):
    if sign == 'add':
        return HttpResponse(num1 + num2)
    if sign == 'sub':
        return HttpResponse(num1 - num2)
    if sign == 'mul':
        return HttpResponse(num1 * num2)
    else:
        return HttpResponse('别乱来啊')


def birth_view(request, year, month, day):
    # print('path_info is', request.path_info)
    # print('method is', request.method)
    # print('GET is', request.GET)
    # print('full path is', request.get_full_path())
    # print('META is',request.META)
    # return HttpResponse('生日是：%s年%s月%s日' % (year, month, day))
    # 相对地址
    return HttpResponseRedirect('/page/1')
    # return HttpResponseRedirect('http://www.baidu.com')


def test_get_post(request):
    # ?a=100&b=20&c=300
    # print('query string is ', request.GET['c'])
    # print(request.GET.get('z', 'no key'))

    # ?a=100&b=200&a=300
    # print(request.GET['a'])  # --> 300
    # print((request.GET.getlist('a', 'no key')))

    # return HttpResponse('test get post is ok')
    if request.method == 'GET':
        return HttpResponse(POST_FORM)
    elif request.method == 'POST':
        return HttpResponse('--Post is OK--')