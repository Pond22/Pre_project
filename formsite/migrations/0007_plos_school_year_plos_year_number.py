# Generated by Django 4.2.4 on 2024-04-22 07:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formsite', '0006_plos_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='plos',
            name='school_year',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3')], default=2567),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plos',
            name='year_number',
            field=models.IntegerField(default=2567, help_text='ใส่ตัวเลขปี 4 ตัว', validators=[django.core.validators.MinValueValidator(1999), django.core.validators.MaxValueValidator(3100)], verbose_name='ปี'),
            preserve_default=False,
        ),
    ]