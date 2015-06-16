# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0002_auto_20150616_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='latitude',
            field=models.DecimalField(null=True, verbose_name='latitude', max_digits=10, decimal_places=7, blank=True),
        ),
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='longitude',
            field=models.DecimalField(null=True, verbose_name='longitude', max_digits=10, decimal_places=7, blank=True),
        ),
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='openstreetmap_id',
            field=models.CharField(unique=True, max_length=255, verbose_name='openstreetmap id', db_index=True),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='wikidata_id',
            field=models.CharField(unique=True, max_length=255, verbose_name='wikidata id', db_index=True),
        ),
        migrations.AlterField(
            model_name='wikidataoccupation',
            name='wikidata_id',
            field=models.CharField(unique=True, max_length=255, verbose_name='wikidata id', db_index=True),
        ),
        migrations.AlterField(
            model_name='wikimediacommonscategory',
            name='wikimedia_commons_id',
            field=models.CharField(unique=True, max_length=255, verbose_name='wikimedia commons id', db_index=True),
        ),
        migrations.AlterField(
            model_name='wikimediacommonsfile',
            name='wikimedia_commons_id',
            field=models.CharField(unique=True, max_length=255, verbose_name='wikimedia commons id', db_index=True),
        ),
    ]
