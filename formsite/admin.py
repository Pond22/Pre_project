from django.contrib import admin
from .models import PLOs,clo,UserEvaluation
# Register your models here.
print("Hello from admin.py")


admin.site.register(PLOs)
admin.site.register(clo)
admin.site.register(UserEvaluation)

