from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField('用户名', max_length=11)
    age = models.IntegerField('年龄')
