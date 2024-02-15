from django.urls import path
from django.shortcuts import  render
from . import views

urlpatterns = [
    path('evaluate/', views.eva_home, name='eva_home'),
    path('evaluate/create_plo', views.create_plo, name='create_plo')
]
