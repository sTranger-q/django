"""

"""

from celery import Celery
from django.conf import settings
import os

# 为celery设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comic_mlgm.settings')

# 创建应用
app = Celery("comic_mlgm_group")
# 配置应用
app.conf.update(
    # 配置broker
    BROKER_URL='redis://:@172.17.0.2:6379/11',
)
# 设置app自动加载任务
app.autodiscover_tasks(settings.INSTALLED_APPS)


