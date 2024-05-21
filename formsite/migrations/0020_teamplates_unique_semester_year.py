# Generated by Django 4.2.4 on 2024-05-21 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formsite', '0019_alter_assessmentresponse_respondent_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='teamplates',
            constraint=models.UniqueConstraint(fields=('semester', 'year_number'), name='unique_semester_year'),
        ),
    ]