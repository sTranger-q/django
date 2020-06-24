from django.urls import path
from . import views
urlpatterns = [
    path('', views.main),
    path('rename', views.rename),
    path('add', views.add_cathpter),
    path('new', views.new),
    path('book', views.book),
    path('chapter/id', views.chapter_id),
    path('chapter/name', views.chapter_name),
    path('ceshi', views.ceshi),
    path('jieba', views.jieba_book),
    path('new_book', views.new_book),
]

