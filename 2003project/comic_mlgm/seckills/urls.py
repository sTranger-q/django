from django.urls import path, include

from . import views

urlpatterns = [
    # http://127.0.0.1:8000/seckill
    path('', views.Seckill.as_view()),
    path('crontab', views.crontab),
    path('time', views.seckill_time),
    # path('ceshi2', views.Seckill().ceshi2),
    # path('ceshi3', views.Seckill().ceshi3),
    path('back', views.back),
    path('result', views.ResultView.as_view()),
    # path('ceshi5', views.ceshi5),
]