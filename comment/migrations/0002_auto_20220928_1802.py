# Generated by Django 3.2.9 on 2022-09-28 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='upvote',
            new_name='like',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='downvote',
        ),
    ]
