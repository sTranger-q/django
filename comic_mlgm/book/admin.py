from django.contrib import admin

from .models import *


# Register your models here.
@admin.register(ComicBook)
class ComicBookManager(admin.ModelAdmin):
    list_display = ['id', 'name', 'writer', 'all_number', 'update_time', 'set_up_time', 'classify', 'is_active']
    list_display_links = ['name']
    list_filter = ['writer', 'is_active']
    search_fields = ['name', 'writer']
    list_editable = ['is_active', 'classify']
    list_per_page = 20



@admin.register(ComicPath)
class ComicPathManager(admin.ModelAdmin):
    list_display = ['id_id', 'open_name', 'vip_name', 'all_number', 'open_number', 'all_number']
    list_display_links = ['id_id']
    search_fields = ['id_id']
    list_editable = ['open_number']
    list_per_page = 20
