# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-03 12:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0010_auto_20160803_1159'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Likes',
            new_name='Like',
        ),
    ]
