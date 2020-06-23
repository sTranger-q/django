import redis
import time

pool = redis.ConnectionPool(host='127.0.0.1', db=2, port=6379,
                            password='z03104299')

r = redis.Redis(connection_pool=pool)


def withpipeline(r):
    p = r.pipeline()
    for i in range(1000):
        key = 'test1' + str(i)
        value = i + 1
        p.set(key, value)
    p.execute()


def withoutpipeline(r):
    for i in range(1000):
        key = 'test2' + str(i)
        value = i + 1
        r.set(key, value)


if __name__ == '__main__':
    t1 = time.time()
    # withpipeline(r)  # 0.02216935157775879
    withoutpipeline(r=r)  # 0.10777640342712402
    print('withpipeline: ', time.time() - t1)
