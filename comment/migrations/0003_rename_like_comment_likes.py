# Generated by Django 3.2.9 on 2022-09-28 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_auto_20220928_1802'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='like',
            new_name='likes',
        ),
    ]
