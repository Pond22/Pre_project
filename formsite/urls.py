from django.urls import path, include
from django.shortcuts import  render
from rest_framework.routers import DefaultRouter
from formsite import views
from .views import *

#router = DefaultRouter()
#router.register(r'csv', CSV_API, basename='csv')


urlpatterns = [
    path('home', views.home, name='home'),
    path('index', views.index, name='index'),
    path('test', views.view_form, name='view_form'),
    path('create_plo', views.create_plo, name='create_plo'),
     path('manage_plos', views.manage_plos, name='manage_plos'),
    #path('', include(router.urls)),
    #path('api-csv/', include('rest_framework.urls', namespace='rest_framework'))
]
