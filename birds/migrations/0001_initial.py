# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-15 18:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family_scientific', models.CharField(max_length=100)),
                ('family_english', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Genus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genus', models.CharField(max_length=100)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='birds.Family')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Sighting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(default=None, max_length=100)),
                ('species_tags', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('lat', models.FloatField(default=None)),
                ('lng', models.FloatField(default=None)),
                ('sighting_date', models.DateTimeField()),
                ('image', models.ImageField(default=None, upload_to=b'')),
                ('user_id', models.IntegerField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('species', models.CharField(default=None, max_length=100)),
                ('species_english', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('genus', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='birds.Genus')),
            ],
        ),
        migrations.CreateModel(
            name='SpeciesFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('species_list', models.FileField(upload_to=b'')),
            ],
        ),
        migrations.CreateModel(
            name='Subspecies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subspecies', models.CharField(max_length=100)),
                ('species', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='birds.Species')),
            ],
        ),
        migrations.AddField(
            model_name='sighting',
            name='subspecies',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='birds.Subspecies'),
        ),
        migrations.AddField(
            model_name='family',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='birds.Order'),
        ),
    ]
