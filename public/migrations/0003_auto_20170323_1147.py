# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-23 11:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0002_auto_20170323_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_name',
            field=models.CharField(max_length=20),
        ),
    ]
