# Generated by Django 4.2.4 on 2024-05-14 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formsite', '0009_form_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='section',
        ),
    ]