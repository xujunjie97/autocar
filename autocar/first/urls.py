"""autocar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static

from autocar import settings
from . import views
app_name = 'first'
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register_view, name='register'),
    url(r'^success$', views.success, name='success'),
    url(r'^userlogin$', views.login),
    url(r'^userlogin/$', views.userlogin_view, name='login'),
    url(r'^modifyPwd$', views.modifyPwd),
    url(r'^modifyPwd/$', views.modifyPwd_view, name='modifyPwd'),
    url(r'^updataImage/$', views.uploadImg),
    url(r'^updataImage2/$', views.uploadImg_view, name='Image'),
    url(r'^userInfo/$', views.userInfo),
    url(r'^userInfo2/$', views.userInfo_view, name='userInfo'),
    url(r'^ordersInfo/$', views.order_view.as_view(), name='order')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

