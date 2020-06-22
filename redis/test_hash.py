import redis

r = redis.Redis(host='127.0.0.1', port=6379, db=0, password='z03104299')
# r.hset('pyh1', 'username', 'wang')
# r.hset('pyh1', 'age', 63)
r.hmset('pyh2', {'username': 'guoxiaonao', 'age': '19'})
print(r.hgetall('pyh2'))
