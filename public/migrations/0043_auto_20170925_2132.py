# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-25 21:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0042_quenstionanswer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quenstionanswer',
            name='answer',
            field=models.TextField(null=True),
        ),
    ]