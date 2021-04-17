# Generated by Django 3.0.4 on 2020-04-07 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20200407_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='designation',
            field=models.CharField(choices=[('hod', 'Hod'), ('faculty', 'Faculty'), ('student', 'Student')], default='faculty', max_length=30),
        ),
    ]
