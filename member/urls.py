from django.urls import path
from django.shortcuts import  render
from . import views

urlpatterns = [
    path('member/', views.member, name='member'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('sign_up', views.sign_up, name='sign_up')
]
