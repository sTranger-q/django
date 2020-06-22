# import redis
#
# r = redis.Redis(host='127.0.0.1', port=6379, db=0, password='z03104299')
#
# key_list = r.keys('*')
# for key in key_list:
#     print(key.decode())
# if r.exists('k2'):
#     print('OK')
# else:
#     print('不OK')
#
# # =========list=========
# r.lpush('l1', 'Tom', 'Jack', 'Lili')
# r.ltrim('l1', -8, -1)
# print(r.lrange('l1', 0, -1))
