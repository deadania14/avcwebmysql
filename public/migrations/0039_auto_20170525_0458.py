# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-25 04:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0038_timeline_writer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='timeline',
            options={'ordering': ['-created_date']},
        ),
    ]
