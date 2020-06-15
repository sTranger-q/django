from django.db import models


# Create your models here.
class Author(models.Model):
    name = models.CharField('作家', max_length=50, default='')

    class Meta:
        verbose_name = '丈夫'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Wife(models.Model):
    name = models.CharField('姓名', max_length=50, default='')
    author = models.OneToOneField(Author, on_delete=models.CASCADE,
                                  verbose_name='作家')

    class Meta:
        verbose_name = '妻子'
        verbose_name_plural = verbose_name
