"""ITOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.views.static import serve

from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, LinkResetUserView, ResetUserView, \
    LogoutView, IndexView
from ITOnline.settings import MEDIA_ROOT, STATIC_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', TemplateView.as_view(template_name="index.html"), name="index"),
    path('', IndexView.as_view(), name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    re_path(r'^captcha/', include('captcha.urls')),
    re_path(r'^active/(?P<email_code>.*)/$', ActiveUserView.as_view(), name="active_user"),
    re_path(r'^reset/(?P<email_code>.*)/$', LinkResetUserView.as_view(), name="link_reset_user"),
    re_path(r'^reset/$', ResetUserView.as_view(), name="reset_user"),
    path('forgetpwd/', ForgetPwdView.as_view(), name="forgetpwd"),
    re_path('media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),

    path("org/", include('organization.urls', namespace='org')),
    path("courses/", include("courses.urls", namespace="courses")),
    path("user_cent/", include("users.urls", namespace="user_cent")),
    re_path('static/(?P<path>.*)', serve, {"document_root": STATIC_ROOT}),
]
