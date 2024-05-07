# tasks.py
from celery import Celery, shared_task
from django.utils import timezone
from models import Form

@shared_task
def my_task(a, b):
    return a + b


'''
def check_form_deadline():
    forms = Form.objects.filter(end_date=timezone.now(), expired=False)
    print("eiei")
    for form in forms:
        form.expired = True
        form.save()
'''

