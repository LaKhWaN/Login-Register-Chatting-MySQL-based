"""loginReg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('login', views.login,name='login'),
    path('loginCheck', views.loginCheck,name='loginCheck'),
    path('register', views.register,name='register'),
    path('registerCheck', views.registerCheck,name='registerCheck'),
    path('searchfriend',views.searchfriend,name="searchfriend"),
    path('makefriend',views.makefriend,name="makefriend"),
    path('searchfriendchat',views.searchfriendchat,name="searchfriendchat"),
    path('livechat',views.livechat,name='livechat'),
    path('msgsent',views.msgsent,name="msgsent"),
    path('friends',views.friendlist,name="friendlist"),
    path('about-us',views.aboutUs,name="about-us")
]
