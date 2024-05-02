from django.contrib import admin
from .models import TemplateData,AssessmentItem,Form, AuthorizedUser, AssessmentResponse, Teamplates, LineTokens
# Register your models here.
print("Hello from admin.py")

class FormAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'create')

admin.site.register(TemplateData)
admin.site.register(AssessmentItem)
admin.site.register(Form, FormAdmin)
admin.site.register(LineTokens)
admin.site.register(AuthorizedUser)
admin.site.register(AssessmentResponse)
admin.site.register(Teamplates)


