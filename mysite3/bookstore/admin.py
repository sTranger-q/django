from django.contrib import admin
from .models import *


# Register your models here.

class BookManager(admin.ModelAdmin):
    list_display = ['id', 'title', 'pub', 'price', 'market_price']
    # 必须在list_display中
    list_display_links = ['title']

    list_filter = ['pub']
    # 根据那些字段查询,模糊查询
    search_fields = ['title']
    # 值必须出现在list_display中,不能在list_display_links里
    list_editable = ['market_price']


class AuthorManager(admin.ModelAdmin):
    list_display = ['id', 'name', 'age']
    list_display_links = ['name']


admin.site.register(Book, BookManager)
admin.site.register(Author, AuthorManager)
