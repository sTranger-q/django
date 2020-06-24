import time

import redis

pool = redis.ConnectionPool(host='127.0.0.1', db=2, port=6379,
                            password='z03104299')

r = redis.Redis(connection_pool=pool)


def double_account(user_id):
    key = 'account_%s' % user_id
    with r.pipeline(transaction=True) as pipe:
        while True:
            try:
                pipe.watch(key)
                limit = r.get(key).decode()

                pipe.multi()
                pipe.incrby(key, limit)
                if input('请确认: ') == '1':
                    pipe.execute()
                    print('Now,the limit is: %s' % r.get(key).decode())
                    break
                else:
                    print('请按1，谢谢')
                    continue

            except redis.WatchError as e:
                print(e)
                # continue


double_account(1)
# print(r.get('account_1'))
