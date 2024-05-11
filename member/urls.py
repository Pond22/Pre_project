from django.urls import path
from django.shortcuts import  render
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('manage_member/', views.manage_member, name='manage_member'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
