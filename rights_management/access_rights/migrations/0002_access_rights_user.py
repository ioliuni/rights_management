# Generated by Django 4.2.2 on 2023-07-28 20:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('access_rights', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='access_rights',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]