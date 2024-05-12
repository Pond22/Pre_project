from django.contrib import admin
from .models import TemplateData,AssessmentItem,Form, AssessmentResponse, Teamplates, Departments, UserProfile, Course, AuthorizedUser, CLO
print("Hello from admin.py")

class FormAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'create')

admin.site.register(TemplateData)
admin.site.register(AssessmentItem)
admin.site.register(Form, FormAdmin)
admin.site.register(Departments)
admin.site.register(AssessmentResponse)
admin.site.register(Teamplates)
admin.site.register(UserProfile)
admin.site.register(Course)
admin.site.register(AuthorizedUser)
admin.site.register(CLO)

