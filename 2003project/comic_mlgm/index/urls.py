from django.contrib import admin
from django.urls import path, include

from index import views

urlpatterns = [
    # http://127.0.0.1:8000/index
    path('', views.index),
    path('details', views.details),
    path('picture', views.picture),
    path('detail/<int:x>', views.details_id),
    path('contents/<int:x>/<int:y>', views.contents),
    path('content/<int:x>/<int:y>/<int:z>', views.content),
    path('screen/<int:x>', views.screen),
    path('search', views.search),
]