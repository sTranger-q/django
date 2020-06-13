from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField('书名', max_length=50, unique=True, default='')
    price = models.DecimalField('定价', max_digits=7, decimal_places=2,
                                default=0.0)
    # 新增字段，必须+default
    pub = models.CharField('出版社', max_length=120, default='')
    market_price = models.DecimalField('零售价', max_digits=6, decimal_places=2,
                                       default=0)
    is_active = models.BooleanField('是否活跃', default=True)

    def __str__(self):
        return 'title:%s pub:%s price:%s market_price:%s' % (self.title,
                                                             self.pub,
                                                             self.price,
                                                             self.market_price)

    class Meta:
        db_table = 'books'


class Author(models.Model):
    name = models.CharField('作者', max_length=30, default='')
    age = models.IntegerField('年龄', default=1)
    email = models.EmailField('邮箱', null=True)
    is_active = models.BooleanField('是否活跃', default=True)

    class Meta:
        db_table = 'author'
