# Generated by Django 3.1.7 on 2021-04-06 01:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0002_auto_20210406_0714'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agenda',
            name='user',
        ),
        migrations.AlterField(
            model_name='agenda',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agenda.users'),
        ),
    ]