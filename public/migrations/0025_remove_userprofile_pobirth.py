# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-04 11:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0024_auto_20170504_1146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='pobirth',
        ),
    ]