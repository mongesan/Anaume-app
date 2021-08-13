# Generated by Django 3.2.5 on 2021-07-24 06:28

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_text_words'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='words',
            field=django_mysql.models.ListCharField(models.CharField(max_length=20), default='', max_length=840, size=40),
        ),
    ]
