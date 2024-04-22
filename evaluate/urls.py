from django.urls import path
from django.shortcuts import  render
from . import views


urlpatterns = [
    path('evaluate/', views.eva_home, name='eva_home'),
    path('evaluate/create_plo', views.create_plo, name='create_plo'),
    path('evaluate/create_form', views.create_form, name='create_form'),
    #เอาไว้ดูรายละเอียดฟอมร์ที่มีทั้งหมด
    path('form/form_detail', views.form_detail, name='form_detail'),
    path('evaluate/create_clo/<int:form_id>/', views.create_clo, name='create_clo'),
    path('form/<int:form_id>/', views.view_form, name='view_form'),
    path('eiei/', views.dy, name='dy'),
]
