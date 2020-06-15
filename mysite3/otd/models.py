from django.db import models


# Create your models here.
class Publisher(models.Model):
    name = models.CharField('出版社', max_length=100, default='', unique=True)

    class Meta:
        verbose_name = '出版社'
        verbose_name_plural = verbose_name


class Book(models.Model):
    title = models.CharField('书名', max_length=50, default='')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE,
                                  verbose_name='出版社')

    class Meta:
        verbose_name = '图书'
        verbose_name_plural = verbose_name
