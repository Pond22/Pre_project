# tasks.py
from celery import shared_task
from django.utils import timezone
from django.utils.timezone import localtime
from .models import *
import requests
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_line_notify(message, token):
    url = 'https://notify-api.line.me/api/notify'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization':'Bearer ' + token
    }
    data = {'message': message}
    response = requests.post(url, headers=headers, data=data)
    return response.status_code, response.text

def send_email_notify(subject, message, recipient_list):
    # เรนเดอร์ HTML template
    html_content = render_to_string('noti_email_template.html', {'subject': subject, 'message': message})

    
    # สร้างอีเมล
    email = EmailMultiAlternatives(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)

@shared_task
def check_expired_forms():
    now = localtime(timezone.now())
    expired_forms = Form.objects.filter(expired=False)
    print(f"เวลาปัจจุบัน {now}")
    for form in expired_forms:
        authorized_users = AuthorizedUser.objects.filter(form=form)
        for authorized_user in authorized_users:
            try:
                user_profile = UserProfile.objects.get(user=authorized_user.users)
                email = user_profile.user.email
                line_token = user_profile.line_token
                """ if form.start_date and form.start_date == now:
                    # Notify for start date
                    message = f"ฟอร์ม {form.name} ถึงเวลาประเมินแล้ว"
                    if line_token:
                        send_line_notify(message, line_token)
                        print(f"Sent LINE notification to {authorized_user.users.username}")
                    if email:
                        send_email_notify("ถึงเวลาประเมินแบบฟอร์ม", message, [email])
                        print(f"Sent email notification to {authorized_user.users.username}") """
                
                if form.end_date and form.end_date <= now:
                    # Notify for end date
                    form.expired = True
                    form.save()
                    message = f"ฟอร์ม {form.name} หมดเวลาแล้ว"
                    if line_token:
                        send_line_notify(message, line_token)
                        print(f"Sent LINE notification to {authorized_user.users.username}")
                    if email:
                        send_email_notify("แบบฟอร์มหมดเวลา", message, [email])
                        print(f"Sent email notification to {authorized_user.users.username}")

                elif form.end_date and (form.end_date - now).days == 1:
                    # Notify for 1 day remaining
                    message = f"ฟอร์ม {form.name} จะหมดเวลาใน 1 วัน"
                    if line_token:
                        send_line_notify(message, line_token)
                        print(f"Sent LINE notification to {authorized_user.users.username}")
                    if email:
                        send_email_notify("แบบฟอร์มจะหมดเวลาใน 1 วัน", message, [email])
                        print(f"Sent email notification to {authorized_user.users.username}")
                
            except UserProfile.DoesNotExist:
                print(f"UserProfile does not exist for user {authorized_user.users.username}")

subject = "Test Email Subject"
message = "This is a test email message."
recipient_list = ["pondba22@gmail.com"]

send_email_notify(subject, message, recipient_list)

'''
def check_form_deadline():
    forms = Form.objects.filter(end_date=timezone.now(), expired=False)
    print("eiei")
    for form in forms:
        form.expired = True
        form.save()
'''

