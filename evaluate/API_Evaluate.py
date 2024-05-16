import json
from formsite.models import *
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *

def get_sections(request, course_id):
    sections = Section.objects.filter(course_id=course_id)
    section_list = [(section.id, section.session_number) for section in sections]
    return JsonResponse(section_list, safe=False)

def API_addnew_tempaltedata (request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form_id = data.get('form_id')
        items = data.get('items')
     
        try:
            form = Form.objects.get(id=form_id)

            # ลบ AssessmentItem จากแม่อบบเก่าออก
            items_to_delete = AssessmentItem.objects.filter(form=form, template_select__isnull=False)
            items_to_delete.delete()
            for item in items:
                parent = None
                if item['isSub']:
                    parent = AssessmentItem.objects.get(id=item_id)
                
                template_select = TemplateData.objects.get(id=item['template_select_id'])
                assessment_item =AssessmentItem.objects.create(
                    text=item['text'],
                    form=form,
                    template_select=template_select,
                    parent=parent
                )
                if item['isSub'] == False :
                    item_id = assessment_item.id
            return JsonResponse({'success': True})
        except Form.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Form not found'})
        except AssessmentItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Parent item not found'})
        except TemplateData.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Template item not found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

#อัพเดตข้อมูล PLO&O ใน Temlplate ที่มีอยู่ก่อน ลบด้วย
def API_updates_delete_form(request):
    if request.method == 'POST':
        data_id = request.POST.get('data_id')
        text = request.POST.get('text')
        data_type = request.POST.get('type')  

        if data_type == 'TemplateData':
            AssessmentItem.objects.filter(id=data_id).update(text=text)
        """ elif data_type == 'CLO':
            CLO.objects.filter(id=data_id).update(text=text) """
        return JsonResponse({'status': 'success', 'message': 'Data updated successfully'})
    
    elif request.method == 'DELETE' :
        data_id = request.GET.get('data_id')
        data_type = request.GET.get('type')  
      
        if data_type == 'TemplateData':
            AssessmentItem.objects.filter(id=data_id).delete()
            print("delete",data_id)
        """ elif data_type == 'CLO':
            CLO.objects.filter(id=data_id).delete() """
        return JsonResponse({'status': 'success', 'message': 'Delete successfully'})
    
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

#เพิ่มข้อมูล PLO&O ใน Temlplate ที่มีอยู่ก่อน เสร็จ
def addnew_form_data(request):
    if request.method == 'POST':
    
        if request.POST.get('type') == "Newparent":
            Form_in = get_object_or_404(Form, id=request.POST.get('form_id')) 
    
            AssessmentItem.objects.create(form = Form_in, text ="")
            return JsonResponse({'status': 'success', 'message': 'Data updated successfully'})
        
        elif request.POST.get('type') != "Newparent":
            parent_id = request.POST.get('data_id').split('_')[2] 
            text = request.POST.get('text')
            print(request.POST.get('text'))
            data_type = request.POST.get('type')
            if text is not None and text.strip() != "" :
                form_in = Form.objects.get(id=request.POST.get('form_id'))
                if data_type == 'TemplateData':
                    # สร้างหรืออัพเดต TemplateData ใหม่
                    AssessmentItem.objects.update_or_create(parent=AssessmentItem.objects.get(id=parent_id), text=text, form = form_in)
                """ elif data_type == 'CLO':
                    # สร้างหรืออัพเดต CLO ใหม่
                    CLO.objects.update_or_create(parent=CLO.objects.get(id=parent_id), text=text, form =form_in)
                return JsonResponse({'status': 'success', 'message': 'Data updated successfully'}) """
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    
def update_form_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form_id = data.get('form_id')
        form_data = data.get('data')
        
        try:
            form_instance = Form.objects.get(id=form_id)
        except Form.DoesNotExist:
            return JsonResponse({'error': 'Form not found'}, status=404)
        
        form = FormUpdateForm(form_data, instance=form_instance)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Form updated successfully'}, status=200)
        else:
            return JsonResponse(form.errors, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
def manage_AuthorizedUser(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form_id = data.get("form_id")
        student_code = data.get("student_code")

        try:
            form_in = Form.objects.get(id=form_id)
        except Form.DoesNotExist:
            return JsonResponse({'error': 'Form not found'}, status=404)

        try:
            user = User.objects.get(username=student_code)
            if AuthorizedUser.objects.filter(users=user, form=form_in).exists():
                return JsonResponse({'error': 'User is already authorized for this form'}, status=400)
        except User.DoesNotExist:
            
            email = f'{student_code}@payap.ac.th'
            user = User.objects.create_user(username=student_code, email=email, password=str(student_code))
            group = Group.objects.get(name='นักศึกษา')
            user.groups.add(group)
            AuthorizedUser.objects.create(form=form_in, users=user)
            return JsonResponse({'message': 'User successfully created and authorized'}, status=201)
     
        user = User.objects.get(username=student_code)
        AuthorizedUser.objects.create(form=form_in, users=user)
        
        return JsonResponse({'User successfully created and authorized'}, status=400)

    if request.method == 'DELETE':
        data = json.loads(request.body)
        aut_id = data['aut_id']
        
        if AuthorizedUser.objects.filter(id=aut_id).exists():
            AuthorizedUser.objects.get(id=aut_id).delete()
        return JsonResponse({'message': 'User deleted successfully'}, status=200)
    return JsonResponse({'error': 'User not found'}, status=404)