# Generated by Django 4.2.2 on 2023-07-26 21:03

from django.db import migrations, models
import django.db.models.deletion
import rights_management.accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0001_initial'),
        ('accounts', '0008_alter_rightsuser_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rightsuser',
            name='department',
            field=models.ForeignKey(default=rights_management.accounts.models.get_depar, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='department.department'),
        ),
    ]
