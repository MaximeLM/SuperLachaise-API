# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivedModification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('target_object_class', models.CharField(max_length=255)),
                ('target_object_id', models.BigIntegerField()),
                ('action', models.CharField(max_length=255, choices=[('create', 'create'), ('modify', 'modify'), ('delete', 'delete')])),
                ('new_values', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LocalizedOpenStreetMapPOI',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('wikipedia', models.CharField(max_length=255, blank=True)),
                ('language', models.ForeignKey(to='superlachaise_api.Language')),
            ],
            options={
                'verbose_name': 'localized OpenStreetMap POI',
                'verbose_name_plural': 'localized OpenStreetMap POIs',
            },
        ),
        migrations.CreateModel(
            name='PendingModification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('target_object_class', models.CharField(max_length=255)),
                ('target_object_id', models.BigIntegerField()),
                ('action', models.CharField(max_length=255, choices=[('create', 'create'), ('modify', 'modify'), ('delete', 'delete')])),
                ('new_values', models.CharField(max_length=255, blank=True)),
                ('apply', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='openstreetmappoilocalization',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='openstreetmappoilocalization',
            name='language',
        ),
        migrations.RemoveField(
            model_name='openstreetmappoilocalization',
            name='openStreetMapPOI',
        ),
        migrations.AlterUniqueTogether(
            name='openstreetmappoilocalizationmodification',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='openstreetmappoilocalizationmodification',
            name='language',
        ),
        migrations.RemoveField(
            model_name='openstreetmappoilocalizationmodification',
            name='openStreetMapPOI',
        ),
        migrations.AlterUniqueTogether(
            name='openstreetmappoimodification',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='openstreetmappoimodification',
            name='openStreetMapPOI',
        ),
        migrations.AlterModelOptions(
            name='openstreetmappoi',
            options={'verbose_name': 'OpenStreetMap POI', 'verbose_name_plural': 'OpenStreetMap POIs'},
        ),
        migrations.DeleteModel(
            name='OpenStreetMapPOILocalization',
        ),
        migrations.DeleteModel(
            name='OpenStreetMapPOILocalizationModification',
        ),
        migrations.DeleteModel(
            name='OpenStreetMapPOIModification',
        ),
        migrations.AlterUniqueTogether(
            name='pendingmodification',
            unique_together=set([('target_object_class', 'target_object_id')]),
        ),
        migrations.AddField(
            model_name='localizedopenstreetmappoi',
            name='openStreetMapPOI',
            field=models.ForeignKey(to='superlachaise_api.OpenStreetMapPOI'),
        ),
        migrations.AlterUniqueTogether(
            name='localizedopenstreetmappoi',
            unique_together=set([('openStreetMapPOI', 'language')]),
        ),
    ]
