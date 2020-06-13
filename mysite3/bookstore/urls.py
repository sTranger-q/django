from django.urls import path

from . import views

urlpatterns = [
    path('all_book', views.all_book),
]
