# Generated by Django 2.2.6 on 2019-12-26 02:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photographer', '0003_auto_20191125_0210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photographer',
            name='zzigsa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photographer', to=settings.AUTH_USER_MODEL),
        ),
    ]
