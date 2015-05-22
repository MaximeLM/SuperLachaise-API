# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('description', models.CharField(max_length=255, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OpenStreetMapPOI',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('latitude', models.DecimalField(max_digits=10, decimal_places=7)),
                ('longitude', models.DecimalField(max_digits=10, decimal_places=7)),
                ('wikidata', models.CharField(max_length=255, blank=True)),
                ('wikimedia_commons', models.CharField(max_length=255, blank=True)),
                ('historic', models.CharField(max_length=255, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OpenStreetMapPOILocalization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wikipedia', models.CharField(max_length=255, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('language', models.ForeignKey(to='superlachaise_api.Language')),
                ('openStreetMapPOI', models.ForeignKey(to='superlachaise_api.OpenStreetMapPOI')),
            ],
        ),
        migrations.CreateModel(
            name='OpenStreetMapPOILocalizationModification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.CharField(max_length=255, choices=[('wikipedia', 'wikipedia')])),
                ('new_value_char', models.CharField(max_length=255, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('language', models.ForeignKey(to='superlachaise_api.Language')),
                ('openStreetMapPOI', models.ForeignKey(to='superlachaise_api.OpenStreetMapPOI')),
            ],
        ),
        migrations.CreateModel(
            name='OpenStreetMapPOIModification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.CharField(max_length=255, choices=[('name', 'name'), ('latitude', 'latitude'), ('longitude', 'longitude'), ('wikidata', 'wikidata'), ('wikimedia_commons', 'wikimedia_commons'), ('historic', 'historic')])),
                ('new_value_char', models.CharField(max_length=255, blank=True)),
                ('new_value_decimal', models.DecimalField(null=True, max_digits=10, decimal_places=7, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('openStreetMapPOI', models.ForeignKey(to='superlachaise_api.OpenStreetMapPOI')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='openstreetmappoimodification',
            unique_together=set([('openStreetMapPOI', 'field')]),
        ),
        migrations.AlterUniqueTogether(
            name='openstreetmappoilocalizationmodification',
            unique_together=set([('openStreetMapPOI', 'language', 'field')]),
        ),
        migrations.AlterUniqueTogether(
            name='openstreetmappoilocalization',
            unique_together=set([('openStreetMapPOI', 'language')]),
        ),
    ]
