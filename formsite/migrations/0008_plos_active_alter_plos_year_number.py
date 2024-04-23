# Generated by Django 4.2.4 on 2024-04-22 09:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formsite', '0007_plos_school_year_plos_year_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='plos',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='plos',
            name='year_number',
            field=models.IntegerField(help_text='ใส่ตัวเลขปี 4 ตัว', validators=[django.core.validators.MinValueValidator(2567), django.core.validators.MaxValueValidator(2570)], verbose_name='ปี'),
        ),
    ]