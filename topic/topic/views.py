from django.http import HttpResponse
import redis

r = redis.Redis(host='127.0.0.1', port=6379, db=2, password='z03104299')


def detail_view(request, bid):
    # sort_set格式储存数据
    book_key = 'topic:read'
    # 判断
    if r.zrank(book_key, bid) is None:
        r.zadd(book_key, {bid: 1})
    else:
        # 可以直接+
        r.zincrby(book_key, 1, bid)
    return HttpResponse('id为%s的小说阅读量为%s' % (bid, r.zscore(book_key, bid)))


def index_view(request):
    # topic_lis = r.zrevrange('topic', 0, 9, withscores=True)
    # print('===========')
    # for book in topic_lis:
    #     print('%s,%s' % (book[0], book[1]))
    all_topic = r.zrevrange('topic:read', 0, 9)
    for n, t_id in enumerate(all_topic):
        n += 1
        print(n, t_id)
    return HttpResponse('aha')
