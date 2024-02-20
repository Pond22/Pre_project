from django.contrib import admin
from .models import PLOs,clo,UserEvaluation,form, students
# Register your models here.
print("Hello from admin.py")

class FormAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'create')

admin.site.register(PLOs)
admin.site.register(clo)
admin.site.register(UserEvaluation)
admin.site.register(form, FormAdmin)
admin.site.register(students)


