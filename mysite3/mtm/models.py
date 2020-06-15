from django.db import models


# Create your models here.
class Author(models.Model):
    name = models.CharField('作家', max_length=50, default='')


class Book(models.Model):
    title = models.CharField('书名', max_length=100, default='')
    authors = models.ManyToManyField(Author)
