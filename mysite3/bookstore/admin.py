from django.contrib import admin
from .models import *


# Register your models here.

class BookManager(admin.ModelAdmin):
    list_display = ['id', 'title', 'pub', 'price', 'market_price']
    list_display_links = ('title',)


admin.site.register(Book, BookManager)
