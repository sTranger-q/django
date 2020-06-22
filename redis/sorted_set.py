import redis

r = redis.Redis(host='127.0.0.1', port=6379, db=0, password='z03104299')

# r.zadd('zz1', {'zj': 900, 'guoxiaonao': 800, 'xiaowang': 1000})
# print(r.zrange('zz1', 0, -1, desc=True, withscores=True))
# print(r.zrevrange('zz1', 0, -1, withscores=True))
# print(r.zrangebyscore('zz1', '800', '1000', withscores=True, start=0, num=2))
# print(r.zrank('zz1', 'zj') + 1)
# print(r.zcount('zz1', 900, '(1000'))
# r.zadd('zz2', {'zj': 900, 'guoxiaonao': 900})
print(r.zrange('zz1', 0, -1, withscores=True))
print(r.zrange('zz2', 0, -1, withscores=True))
# r.zinterstore('zz3', ('zz1', 'zz2'), aggregate='MAX')
print(r.zrange('zz3', 0, -1, withscores=True))
# r.zunionstore('zz4', ('zz1', 'zz2'), aggregate='MIN')
print(r.zrange('zz4', 0, -1, withscores=True))
