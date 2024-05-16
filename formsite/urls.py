from django.urls import path, include
from django.shortcuts import  render
from rest_framework.routers import DefaultRouter
from formsite import views
from .views import *
from .formsite_API import *

#router = DefaultRouter()
#router.register(r'csv', CSV_API, basename='csv')


urlpatterns = [
    path('home', views.home, name='home'),
    path('index', views.index, name='index'),
    path('test', views.view_form, name='view_form'),
    path('create_plo', views.create_plo, name='create_plo'),
    path('manage_template', views.manage_template, name='manage_template'),
    path('edit_template/<int:form_id>/', edit_template, name='edit_template'),
    path('delete_update_template_data/', delete_update_template_data, name='delete_update_template_data'),
    path('addnew_template_data/', addnew_template_data, name='addnew_template_data'),
    path('set_active/', set_active, name='set_active'),  #set_active แม่แบบ
    #path('', include(router.urls)),
    #path('api-csv/', include('rest_framework.urls', namespace='rest_framework'))
]
