# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-28 09:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manajemen', '0038_auto_20170527_0148'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='practiceattendance',
            options={'ordering': ['-updated_date']},
        ),
    ]
