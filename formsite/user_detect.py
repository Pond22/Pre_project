from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import HttpResponse
from django.contrib.auth.models import User, Group

def user_is_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists() or user.is_superuser

def group_required(group_name):
    def decorator(view_func):
        @user_passes_test(lambda user: user_is_in_group(user, group_name))
        def _wrapped_view(request, *args, **kwargs):
            if not user_is_in_group(request.user, group_name):
                return HttpResponse(f"{group_name} ONLY!")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

teacher_required = group_required('อาจารย์')
student_required = group_required('นักศึกษา')
committee_required = group_required('กรรมการ')
admin_required = group_required('หัวหน้าสาขา')