# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminCommand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('last_executed', models.DateTimeField(null=True)),
                ('last_result', models.TextField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OpenStreetMapPOI',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=255, choices=[(b'node', b'node'), (b'way', b'way'), (b'relation', b'relation')])),
                ('name', models.CharField(max_length=255)),
                ('latitude', models.DecimalField(max_digits=10, decimal_places=7)),
                ('longitude', models.DecimalField(max_digits=10, decimal_places=7)),
                ('wikipedia', models.CharField(max_length=255, blank=True)),
                ('wikidata', models.CharField(max_length=255, blank=True)),
                ('wikimedia_commons', models.CharField(max_length=255, blank=True)),
                ('historic', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'verbose_name': 'OpenStreetMap POI',
                'verbose_name_plural': 'OpenStreetMap POIs',
            },
        ),
        migrations.CreateModel(
            name='PendingModification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('target_object_class', models.CharField(max_length=255, choices=[(b'OpenStreetMapPOI', 'OpenStreetMap POI')])),
                ('target_object_id', models.BigIntegerField()),
                ('action', models.CharField(max_length=255, choices=[(b'create', 'create'), (b'modify', 'modify'), (b'delete', 'delete')])),
                ('modified_fields', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(max_length=255)),
                ('key', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255, blank=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='setting',
            unique_together=set([('category', 'key')]),
        ),
        migrations.AlterUniqueTogether(
            name='pendingmodification',
            unique_together=set([('target_object_class', 'target_object_id')]),
        ),
    ]
