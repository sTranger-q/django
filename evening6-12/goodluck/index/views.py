import random
from django.shortcuts import render


# Create your views here.
def index_view(request):
    if request.method == 'GET':
        # 存放所有奖品列表

        lis = []
        for i in range(1, 9):
            lis.append('/static/images/prize%d.jpg' % i)
        # 随机列表
        random.shuffle(lis)
        return render(request, 'index.html',
                      {'prizes': lis,

                       })


def prize_view(request):
    return render(request, 'prize.html')
