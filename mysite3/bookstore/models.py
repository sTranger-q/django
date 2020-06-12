from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField('书名', max_length=50, default='')
    price = models.DecimalField('定价', max_digits=7, decimal_places=2,
                                default=0.0)
    # 新增字段，必须+default
    pub = models.CharField('出版社', max_length=120, default='')

    class Meta:
        db_table = 'book'
