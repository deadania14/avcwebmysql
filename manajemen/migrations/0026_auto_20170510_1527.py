# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-10 15:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manajemen', '0025_logkelas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logkelas',
            name='last_kelas',
        ),
        migrations.RemoveField(
            model_name='logkelas',
            name='new_kelas',
        ),
        migrations.RemoveField(
            model_name='logkelas',
            name='user',
        ),
        migrations.DeleteModel(
            name='LogKelas',
        ),
    ]