# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-25 14:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('birds', '0018_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sighting',
            name='user_id',
        ),
        migrations.AddField(
            model_name='sighting',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
