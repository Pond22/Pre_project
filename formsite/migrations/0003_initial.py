# Generated by Django 4.2.4 on 2024-02-13 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('formsite', '0002_remove_answer_question_remove_clo_created_by_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(default=2024)),
                ('school_year', models.IntegerField(choices=[(1, '1'), (2, '2')])),
            ],
        ),
    ]
