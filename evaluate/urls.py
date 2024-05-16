from django.urls import path
from django.shortcuts import  render
from . import views
from .API_Evaluate import *

urlpatterns = [
    path('evaluate/', views.eva_home, name='eva_home'),
    path('evaluate_form/<int:form_id>/', views.evaluate_form, name='evaluate_form'),
    path('evaluate/create_plo', views.create_plo, name='create_plo'),
    path('evaluate/create_form', views.create_form, name='create_form'),
    #เอาไว้ดูรายละเอียดฟอมร์ที่มีทั้งหมด
    path('form/form_detail', views.form_detail, name='form_detail'),
    path('evaluate/create_clo/<int:form_id>/', views.create_clo, name='create_clo'),
    path('form/<int:form_id>/', views.view_form, name='view_form'),
    path('edit_form/<int:form_id>/', views.edit_form, name='edit_form'),
    path('save-new-items/', API_addnew_tempaltedata, name='API_addnew_tempaltedata'),
    path('addnew_form_data/', addnew_form_data, name='addnew_form_data'),
    path('API_updates_delete_form/', API_updates_delete_form, name='API_updates_delete_form'),
    path('update_form_api/', update_form_api, name='update_form_api'),
    path('manage_AuthorizedUser/', manage_AuthorizedUser, name='manage_AuthorizedUser'),#api user
    path('get_sections/<int:course_id>/', get_sections, name='get_sections'),
 
    
]
