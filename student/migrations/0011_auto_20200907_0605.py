# Generated by Django 3.0.6 on 2020-09-07 00:35

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0010_auto_20200906_1318'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='batch',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
