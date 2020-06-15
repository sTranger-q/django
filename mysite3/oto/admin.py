from django.contrib import admin
from .models import *


# Register your models here.
class AuthorManager(admin.ModelAdmin):
    list_display = ['id', 'name']


class WifeManager(admin.ModelAdmin):
    list_display = ['id', 'name', 'author']
    search_fields = ['name']


admin.site.register(Author, AuthorManager)
admin.site.register(Wife, WifeManager)
