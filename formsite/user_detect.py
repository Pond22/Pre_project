from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import HttpResponse
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect

def user_is_in_group(user, group_names):
    return any(user.groups.filter(name=group_name).exists() for group_name in group_names) or user.is_superuser

def group_required(*group_names, redirect_to='/sign_in'):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not user_is_in_group(request.user, group_names):
                return redirect(redirect_to)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

teacher_required = group_required('อาจารย์')
student_required = group_required('นักศึกษา')
committee_required = group_required('กรรมการ')
admin_required = group_required('หัวหน้าสาขา')
committee_or_teacher_required = group_required('กรรมการ', 'อาจารย์')
teacher_or_student_required = group_required('อาจารย์','นักศึกษา' )