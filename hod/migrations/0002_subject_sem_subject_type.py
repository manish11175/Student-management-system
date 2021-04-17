# Generated by Django 3.0.6 on 2020-06-15 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hod', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject_sem',
            name='subject_type',
            field=models.CharField(choices=[('theory', 'Theory'), ('practical', 'Practical'), ('minor project', 'Minor Project'), ('major project', 'Major Project')], default='theory', max_length=30),
        ),
    ]