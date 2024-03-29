# Generated by Django 4.2.4 on 2024-02-29 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('formsite', '0003_form_stu_list'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='form',
            name='stu_list',
        ),
        migrations.CreateModel(
            name='AuthorizedUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stu_list', models.CharField(max_length=10)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formsite.form')),
            ],
        ),
    ]
