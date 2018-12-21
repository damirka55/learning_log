"""Определяет схемы URl для пользователей."""

from django.conf.urls import url
from django.contrib.auth import login
from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.login, name='login')
]
