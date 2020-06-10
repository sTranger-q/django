"""mysite1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from . import views

reg_birth = r'^birthday/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})$'
reg_birth2 = r'^birthday/(?P<day>\d{1,2})/(?P<month>\d{1,2})/(?P<year>\d{4})$'

urlpatterns = [
    path('admin/', admin.site.urls),
    # http://127.0.0.1:8000/page/2003
    path('page/2003', views.page_2003_view),
    path('', views.index_view),
    path('page/1', views.page1_view),
    path('page/2', views.page2_view),
    path('page/<int:page>', views.page_view),
    path('<int:num1>/<str:sign>/<int:num2>', views.calculator_view),
    re_path(reg_birth, views.birth_view),
    re_path(reg_birth2, views.birth_view),
    path('test_get_post', views.test_get_post)
]
