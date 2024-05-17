# tasks.py
from celery import shared_task
from django.utils import timezone
from django.utils.timezone import localtime
from .models import *
import requests

def send_line_notify(message, token):
    url = 'https://notify-api.line.me/api/notify'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization':'Bearer ' + token
    }
    data = {'message': message}
    response = requests.post(url, headers=headers, data=data)
    return response.status_code, response.text

@shared_task
def check_expired_forms():
    now = localtime(timezone.now())
    expired_forms = Form.objects.filter(expired=False)
    print(f"เวลาปัจจุบัน {now}")
    for form in expired_forms:
        if form.end_date and form.end_date <= now: 
            form.expired = True
            form.save()
            message = f"ฟอร์ม {form.name} หมดเวลา"
            authorized_users = AuthorizedUser.objects.filter(form=form)
            
            for authorized_user in authorized_users:
                try:
                    user_profile = UserProfile.objects.get(user=authorized_user.users)
                    print("ine ====",{user_profile.line_token})
                    if user_profile.line_token:
                        send_line_notify(message, user_profile.line_token)
                        print(f"Sent notification to {authorized_user.users.username}")
                except UserProfile.DoesNotExist:
                    print(f"UserProfile does not exist for user {authorized_user.users.username}")
        else:
            message = "Form {{form.id}} has not expired yet or end_date is None."
            authorized_users = AuthorizedUser.objects.filter(form=form)
  
            for authorized_user in authorized_users:
                try:
                    user_profile = UserProfile.objects.get(user=authorized_user.users)
                    print("ine ====",{user_profile.line_token})
                    if user_profile.line_token:
                        send_line_notify(message, user_profile.line_token)
                        print(f"Sent notification to {authorized_user.users.username}")
                except UserProfile.DoesNotExist:
                    print(f"UserProfile does not exist for user {authorized_user.users.username}")


'''
def check_form_deadline():
    forms = Form.objects.filter(end_date=timezone.now(), expired=False)
    print("eiei")
    for form in forms:
        form.expired = True
        form.save()
'''

