# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-27 01:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manajemen', '0037_auto_20170525_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logkelas',
            name='kelas_before',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='log_kelas_before', to='manajemen.Kelas'),
        ),
    ]
