from django.urls import path
from django.shortcuts import  render
from formsite import views

urlpatterns = [
    path('', views.home, name='home'),
    path('index', views.index, name='index')
]
