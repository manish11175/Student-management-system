# Generated by Django 3.0.6 on 2020-06-05 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_adminprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='designation',
            field=models.CharField(choices=[('hod', 'Hod'), ('hod1', 'hod1'), ('faculty', 'Faculty')], default='faculty', max_length=30),
        ),
    ]
