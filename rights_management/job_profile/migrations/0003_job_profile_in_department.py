# Generated by Django 4.2.2 on 2023-08-04 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0002_department_owner'),
        ('job_profile', '0002_job_profile_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='job_profile',
            name='in_department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='department.department'),
        ),
    ]
