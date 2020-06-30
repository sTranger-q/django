from django.db import models


# Create your models here.
class UserProfile(models.Model):
    # avatar可以为空
    # 表名 user_user_profile
    username = models.CharField('用户名', max_length=11, primary_key=True)
    nickname = models.CharField('昵称', max_length=30)
    email = models.EmailField('邮箱', max_length=50)
    password = models.CharField('密码', max_length=32)
    sign = models.CharField('个性签名', max_length=50)
    info = models.CharField('信息', max_length=150)
    avatar = models.ImageField('头像', upload_to='avatar', null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('上次更新', auto_now=True)

    class Meta:
        db_table = 'user_user_profile'
