from django.db import models

# Create your models here.

# class User(models.Model):
#     username = models.CharField("用户名", max_length=30, unique=True)
#     password = models.CharField("密码", max_length=32)
#     created_time = models.DateTimeField('创建时间', auto_now_add=True)
#     updated_time = models.DateTimeField('更新时间', auto_now=True)
#
#     def __str__(self):
#         return "用户" + self.username
#
#
#
# class Works(models.Model):
#     title = models.CharField('标题', max_length=100)
#     content = models.TextField('内容')
#     created_time = models.DateTimeField('创建时间', auto_now_add=True)
#     updated_time = models.DateTimeField('更新时间', auto_now=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)