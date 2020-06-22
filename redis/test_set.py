import redis

r = redis.Redis(host='127.0.0.1', port=6379, db=0, password='z03104299')

r.sadd('pys2', 'a', 'b')
r.sadd('pys3', 'c', 'b')
r.sadd('pys4', 'c', 'b', 'd')

print(r.sinter('pys2', 'pys3', 'pys4'))
print(r.sunionstore('pys5', 'pys2', 'pys3', 'pys4'))
