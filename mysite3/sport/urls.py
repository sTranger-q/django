from django.urls import path

from sport import views

urlpatterns = [
    path('index', views.index_view),
]
