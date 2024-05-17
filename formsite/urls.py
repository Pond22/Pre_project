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
    path('create_plo', views.create_plo, name='create_plo'), #u
    path('manage_template', views.manage_template, name='manage_template'), #u
    path('manage_course', views.manage_course, name='manage_course'), #u
    path('edit_template/<int:form_id>/', edit_template, name='edit_template'), #u
    path('delete_update_template_data/', delete_update_template_data, name='delete_update_template_data'), #u
    path('addnew_template_data/', addnew_template_data, name='addnew_template_data'), #u
    path('set_active/', set_active, name='set_active'),  #set_active แม่แบบ
    path('manage_courses_API/', manage_courses_API, name='manage_courses_API'),  #api จัดการวิชา
    path('delete_course_API/<int:id>/', delete_course_API, name='delete_course_API'), #u
    #path('', include(router.urls)),
    #path('api-csv/', include('rest_framework.urls', namespace='rest_framework'))
]
