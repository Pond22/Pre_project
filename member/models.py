from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission
'''
class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')
    
    def save(self, *args, **kwargs):
        if not self.username:  # ตรวจสอบว่า username ว่างหรือไม่
            self.username = self.email[:10] if self.email else ''  # กำหนด self.username จาก self.email ถ้ามีค่า
        super().save(*args, **kwargs)
        '''