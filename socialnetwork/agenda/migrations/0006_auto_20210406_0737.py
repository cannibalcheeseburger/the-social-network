# Generated by Django 3.1.7 on 2021-04-06 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0005_aye_nay'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='registeredAt',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
