# 结构与主路由一样
from django.urls import path

from music import views

urlpatterns = [
    # http://127.0.0.1:8000/music/index
    path('index', views.music_index),
]
