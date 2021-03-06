# Generated by Django 3.0.6 on 2020-09-04 05:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_auto_20200615_2147'),
        ('hod', '0014_teacherpracticalmark'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherProjectMark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_type', models.CharField(choices=[('minor', 'minor'), ('major', 'major')], default='minor', max_length=20)),
                ('total_mark', models.FloatField()),
                ('obtain_mark', models.FloatField()),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Student')),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hod.Subject_sem')),
            ],
        ),
    ]
