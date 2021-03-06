# Generated by Django 3.0.6 on 2020-06-15 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0008_auto_20200615_2147'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject_sem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept', models.CharField(choices=[('cs', 'CS'), ('it', 'IT'), ('ce', 'CE'), ('me', 'ME'), ('ec', 'EC'), ('ee', 'EE')], default='cs', max_length=10)),
                ('sem', models.CharField(choices=[('1', 'I'), ('2', 'II'), ('3', 'III'), ('4', 'IV'), ('5', 'V'), ('6', 'VI'), ('7', 'VII'), ('8', 'VIII')], default='I', max_length=2)),
                ('subject_name', models.CharField(default='', max_length=100)),
                ('subject_code', models.CharField(default='', max_length=20)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.batch')),
            ],
            options={
                'unique_together': {('year', 'dept', 'sem', 'subject_code')},
            },
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.CharField(choices=[('cs', 'CS'), ('it', 'IT'), ('ce', 'CE'), ('me', 'ME'), ('ec', 'EC'), ('ee', 'EE')], default='cs', max_length=10)),
                ('sem', models.CharField(choices=[('1', 'I'), ('2', 'II'), ('3', 'III'), ('4', 'IV'), ('5', 'V'), ('6', 'VI'), ('7', 'VII'), ('8', 'VIII')], default='I', max_length=2)),
                ('sec', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], default='A', max_length=2)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.batch')),
            ],
            options={
                'unique_together': {('year', 'branch', 'sem', 'sec')},
            },
        ),
    ]
