from django.urls import path
from django.shortcuts import  render
from . import views
from .API_Evaluate import *

urlpatterns = [
    path('evaluate/', views.eva_home, name='eva_home'),#u
    path('evaluate_form/<int:form_id>/', views.evaluate_form, name='evaluate_form'),#u
    path('evaluate/create_form', views.create_form, name='create_form'),#u
    #เอาไว้ดูรายละเอียดฟอมร์ที่มีทั้งหมด
    path('form/form_detail', views.form_detail, name='form_detail'),#u
    path('form/<int:form_id>/', views.view_form, name='view_form'),#u
    path('edit_form/<int:form_id>/', views.edit_form, name='edit_form'), #u
    path('save-new-items/', API_addnew_tempaltedata, name='API_addnew_tempaltedata'),#u API ไม่ต้องทำอะไร
    path('addnew_form_data/', addnew_form_data, name='addnew_form_data'),#u API ไม่ต้องทำอะไร
    path('API_updates_delete_form/', API_updates_delete_form, name='API_updates_delete_form'),#u API ไม่ต้องทำอะไร
    path('update_form_api/', update_form_api, name='update_form_api'),#u API ไม่ต้องทำอะไร
    path('manage_AuthorizedUser/', manage_AuthorizedUser, name='manage_AuthorizedUser'),#api user #u API ไม่ต้องทำอะไร
    path('get_sections/<int:course_id>/', get_sections, name='get_sections'),#u API ไม่ต้องทำอะไร
 
    
]
