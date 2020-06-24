from django.urls import path

from user import views

urlpatterns = [
    # 注册：/user/register
    path("register", views.register_view),
    path("register_server", views.register_server_view),
    path("send_verification_code",views.send_verification_code_view),
    # 登录：/user/login
    path("login", views.login_view),
    path("login_server", views.login_server_view),
    # 忘记密码,找回密码：/user/retrieve_passwd
    path("retrieve_passwd", views.retrieve_view),
    path("verify_user_by_email", views.verify_user_by_email_view),
    path("verify_code", views.verify_code_view),
    path("reset_password", views.reset_password_view),
    # # 微博第三方授权登录：/user/weibo_login
    # path("weibo_login", views.weibo_login_view),
]
