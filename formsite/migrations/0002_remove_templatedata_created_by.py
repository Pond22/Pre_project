# Generated by Django 4.2.4 on 2024-05-02 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formsite', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='templatedata',
            name='created_by',
        ),
    ]