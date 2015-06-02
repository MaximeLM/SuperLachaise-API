# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0080_auto_20150602_1839'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuperLachaiseWikidataRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('type', models.CharField(max_length=255, verbose_name='type', blank=True)),
            ],
            options={
                'ordering': ['superlachaise_poi', 'type', 'wikidata_entry'],
                'verbose_name': 'wikidata entry',
                'verbose_name_plural': 'wikidata entries',
            },
        ),
        migrations.RemoveField(
            model_name='superlachaisepoiwikidataentryrelation',
            name='superlachaise_poi',
        ),
        migrations.RemoveField(
            model_name='superlachaisepoiwikidataentryrelation',
            name='wikidata_entry',
        ),
        migrations.AlterField(
            model_name='superlachaisepoi',
            name='wikidata_entries',
            field=models.ManyToManyField(related_name='superlachaise_pois', verbose_name='wikidata entries', through='superlachaise_api.SuperLachaiseWikidataRelation', to='superlachaise_api.WikidataEntry'),
        ),
        migrations.DeleteModel(
            name='SuperLachaisePOIWikidataEntryRelation',
        ),
        migrations.AddField(
            model_name='superlachaisewikidatarelation',
            name='superlachaise_poi',
            field=models.ForeignKey(verbose_name='superlachaise poi', to='superlachaise_api.SuperLachaisePOI'),
        ),
        migrations.AddField(
            model_name='superlachaisewikidatarelation',
            name='wikidata_entry',
            field=models.ForeignKey(verbose_name='wikidata entry', to='superlachaise_api.WikidataEntry'),
        ),
    ]
