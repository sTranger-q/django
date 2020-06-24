from django.db import models

# Create your models here.
from django.utils import timezone


class ComicBook(models.Model):
    name = models.CharField('名字', max_length=30)
    writer = models.CharField('作者', max_length=20)
    all_number = models.IntegerField('总章节数')
    update_time = models.DateField('更新时间', auto_now=True)
    set_up_time = models.DateField('创建时间', auto_now_add=True)
    is_active = models.BooleanField('授权', default=0)
    classify = models.IntegerField('标签',default=1)



class ComicPath(models.Model):
    id = models.OneToOneField(ComicBook, on_delete=models.PROTECT, primary_key=True)
    open_name = models.CharField('免费dir', max_length=100, default='open')
    vip_name = models.CharField('会员dir', max_length=100, default='vip')
    open_number = models.IntegerField('免费章节数', default=9999)
    # database_path = models.CharField('此书库名',max_length=20,default='comic_book')
    # table_path = models.CharField('此书表名',max_length=20,default='book_picturename')
    all_number = models.IntegerField('总章节数')



class PictureName(models.Model):
    pictureID = models.BigIntegerField('图片ID', primary_key=True)
    picture_name = models.CharField('图片名字', max_length=50)

