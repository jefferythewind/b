# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-09 17:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0022_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='birdphoto',
            name='thumbnail_url',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
    ]