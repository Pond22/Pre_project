# Generated by Django 4.2.4 on 2024-02-20 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formsite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='students',
            fields=[
                ('students_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80)),
            ],
        ),
        migrations.DeleteModel(
            name='test',
        ),
    ]
