# Generated by Django 3.2.5 on 2021-08-13 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_fav_note_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fav',
            old_name='note_id',
            new_name='note',
        ),
    ]
