# Generated by Django 3.2.5 on 2021-07-19 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='desc',
        ),
        migrations.RemoveField(
            model_name='note',
            name='public',
        ),
        migrations.RemoveField(
            model_name='note',
            name='title',
        ),
    ]
