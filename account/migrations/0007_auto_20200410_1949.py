# Generated by Django 3.0.4 on 2020-04-10 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20200410_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='batch',
            field=models.IntegerField(default=''),
        ),
    ]