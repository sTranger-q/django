from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_view),
    path('add', views.add_view),
    path('mod/<int:nid>', views.mod_view),
    path('del/<int:nid>', views.del_view),

]
