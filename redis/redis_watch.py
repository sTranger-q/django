import redis

pool = redis.ConnectionPool(host='127.0.0.1', db=2, port=6379,
                            password='z03104299')

r = redis.Redis(connection_pool=pool)

r.set('credit_card', '500')


def double_account(user_id):
    key = 'account_%s' % user_id
    with r.pipeline(transaction=True) as pipe:
        pass
