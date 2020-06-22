import redis

r = redis.Redis(host='127.0.0.1', port=6379, db=3, password='z03104299')

while True:
    msg = r.blpop('pypc', 10)
    if msg:
        task_str = msg[1].decode()
        task_lis = task_str.split('_')
        for task in task_lis:
            print(task)
        break
    print(msg)
