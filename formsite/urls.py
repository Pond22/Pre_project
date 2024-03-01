from django.urls import path
from django.shortcuts import  render
from formsite import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('index', views.index, name='index'),
    path('test', views.view_form, name='view_form')
]
