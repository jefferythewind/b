# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-15 14:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0006_auto_20160614_1008'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpeciesFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('species_list', models.FileField(upload_to=b'')),
            ],
        ),
    ]
