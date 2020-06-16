"""mysite3 URL Configuration

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
from django.urls import path

from mysite3 import views
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test_static', views.test_static),
    # http:127.0.0.1:8000/music/xxxx-->music应用处理
    path('music/', include('music.urls')),
    path('sport/', include('sport.urls')),
    path('news/', include('news.urls')),
    path('bookstore/', include('bookstore.urls')),
    path('set_cookies', views.test_set_cookies),
    path('get_cookies', views.test_get_cookies),
    path('set_session', views.set_sessions),
    path('get_session', views.get_sessions),
]
