# Generated by Django 3.0.6 on 2020-09-06 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_auto_20200615_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='dob',
            field=models.DateField(blank=True, default=''),
        ),
    ]
