# Generated by Django 3.1.7 on 2021-04-22 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0003_auto_20210422_1751'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userfollowing',
            old_name='following',
            new_name='following_user',
        ),
    ]
