# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-06 08:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('manajemen', '0005_auto_20170406_0813'),
    ]

    operations = [
        migrations.AddField(
            model_name='practiceattendance',
            name='tutor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tutor_practice_attendances', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='practiceattendance',
            name='tutor_pendamping',
            field=models.ManyToManyField(related_name='tutor_pendamping_practice_attendances', to=settings.AUTH_USER_MODEL),
        ),
    ]
