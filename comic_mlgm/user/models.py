from django.db import models

# Create your models here.

# 用户注册登录表
class Users(models.Model):
    user_Name = models.CharField(verbose_name="用户名", max_length=30, unique=True)
    password = models.CharField(verbose_name="密码", max_length=32)
    user_Email= models.EmailField(verbose_name="邮箱", max_length=30)
    vip = models.DateTimeField(verbose_name="VIP有效期", auto_now_add=True)
    is_active = models.BooleanField(verbose_name="是否存在", default=True)
    user_created_Time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    user_updated_Time = models.DateTimeField(verbose_name='更新时间', auto_now=True)


# # 用户个人信息表
class User_Profile(models.Model):
    username = models.OneToOneField(Users, on_delete=models.CASCADE)
    nick_Name = models.CharField(verbose_name="昵称", max_length=30, unique=True)
    user_Type = models.CharField(verbose_name="用户类型", max_length=30)
    career= models.CharField(verbose_name="职业", max_length=30)
    user_Addr= models.CharField(verbose_name="用户地址", max_length=100)
    gender= models.BooleanField(verbose_name="性别",null=True)
    birth= models.DateField(verbose_name='生日',auto_now_add=True)
    portrait=models.ImageField(verbose_name='头像',max_length=100,null=True)
    profile_created_Time=models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    profile_updated_Time=models.DateTimeField(verbose_name='更新时间', auto_now=True)


# 用户身份表
class User_Identity(models.Model):
    username = models.OneToOneField(Users, on_delete=models.CASCADE)
    moderator_id=models.CharField(verbose_name="吧主编号", max_length=30, unique=True,null=True)
    administrater_id=models.CharField(verbose_name="管理员编号", max_length=30, unique=True,null=True)
    administrater_Group=models.CharField(verbose_name="所属管理员分组", max_length=30)
    id_created_Time=models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    id_updated_Time=models.DateTimeField(verbose_name='更新时间', auto_now=True)