import redis

r = redis.Redis(host='127.0.0.1', port=6379, db=3, password='z03104299')

# 任务类型(email)_发件人_收件人_内容
task_str = '%s_%s_%s_%s' % ('email', 'zj', 'gxn', 'content')

r.lpush('pypc', task_str)
