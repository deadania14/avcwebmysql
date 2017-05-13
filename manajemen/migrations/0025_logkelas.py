# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-10 14:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('manajemen', '0024_article_is_concertarticle'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogKelas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(default=django.utils.timezone.now)),
                ('last_kelas', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='log_before', to='manajemen.Kelas')),
                ('new_kelas', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='log_after', to='manajemen.Kelas')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
