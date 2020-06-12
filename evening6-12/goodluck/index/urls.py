from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view),
    path('prize',views.prize_view)
]
