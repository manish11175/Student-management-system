# Generated by Django 3.0.6 on 2020-07-31 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_auto_20200615_2147'),
        ('hod', '0008_auto_20200713_1636'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherSubjectAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default='')),
                ('attend', models.FloatField(choices=[(1, 'present'), (0, 'absent'), (0.5, 'half_day')], default=0, max_length=5)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Student')),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hod.Subject_sem')),
            ],
            options={
                'unique_together': {('student_id', 'subject_id', 'date')},
            },
        ),
    ]