# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-11 04:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manajemen', '0009_auto_20170411_0322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='administrasi',
            name='nominal',
        ),
        migrations.AlterField(
            model_name='administrasi',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='administrasi', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='administrationtype',
            name='paymentstype',
            field=models.CharField(max_length=50),
        ),
    ]
