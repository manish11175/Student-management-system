# Generated by Django 3.0.4 on 2020-04-10 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20200410_2237'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='account',
            new_name='activate',
        ),
        migrations.RenameField(
            model_name='studentprofile',
            old_name='account',
            new_name='activate',
        ),
    ]
