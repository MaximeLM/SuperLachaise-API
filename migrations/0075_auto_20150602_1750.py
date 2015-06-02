# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0074_auto_20150602_1702'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuperLachaisePOI',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('main_image', models.ForeignKey(related_name='superlachaise_pois', verbose_name='main image', to='superlachaise_api.WikimediaCommonsFile', null=True)),
                ('openstreetmap_element', models.OneToOneField(related_name='superlachaise_poi', verbose_name='openstreetmap element', to='superlachaise_api.OpenStreetMapElement')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SuperLachaisePOIWikidataEntryRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('type', models.CharField(max_length=255, verbose_name='type', blank=True)),
                ('superlachaise_poi', models.ForeignKey(verbose_name='superlachaise poi', to='superlachaise_api.SuperLachaisePOI')),
                ('wikidata_entry', models.ForeignKey(verbose_name='wikidata entry', to='superlachaise_api.WikidataEntry')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='superlachaisepoi',
            name='wikidata_entries',
            field=models.ManyToManyField(related_name='superlachaise_pois', verbose_name='wikidata entries', through='superlachaise_api.SuperLachaisePOIWikidataEntryRelation', to='superlachaise_api.WikidataEntry'),
        ),
        migrations.AddField(
            model_name='superlachaisepoi',
            name='wikimedia_commons_category',
            field=models.ForeignKey(related_name='superlachaise_pois', verbose_name='wikimedia commons category', to='superlachaise_api.WikimediaCommonsCategory', null=True),
        ),
    ]
