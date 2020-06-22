from django.urls import path
from . import views

urlpatterns = [
    path('detail/<int:user_id>', views.detail_view),
    path('update/<int:user_id>', views.update_view),
]
