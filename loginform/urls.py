"""myforms URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from . import views
app_name = 'loginform'
urlpatterns = [
    url(r'SignUp/',views.SignUp.as_view(), name='signup'),
    url(r'Login/',views.LoginPage.as_view(), name='login'),
    url(r'logout/',views.logout_page, name='logout'),
    url(r'^book/', include([
        url(r'^create/$', views.AddBook.as_view(), name='book_create'),
        url(r'^delete/(?P<pk>[0-9]+)', views.DeleteBook.as_view(), name='book_delete'),
        url(r'^update/(?P<pk>[0-9]+)', views.UpdateBookDetail.as_view(), name='book_update'),
        url(r'^book-details/(?P<pk>[0-9]+)/', views.BookDetail.as_view(), name='book_detail'),
    ])),
    url(r'^homepage/',views.HomePage.as_view(), name='book_list'),

]
