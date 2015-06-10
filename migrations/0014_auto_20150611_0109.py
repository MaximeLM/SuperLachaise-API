# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0013_auto_20150610_1720'),
    ]

    operations = [
        migrations.CreateModel(
            name='WikidataOccupation',
            fields=[
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('id', models.CharField(max_length=255, serialize=False, verbose_name='id', primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='nom', blank=True)),
                ('superlachaise_category', models.ForeignKey(related_name='wikidata_occupations', verbose_name='cat\xe9gorie SuperLachaise', blank=True, to='superlachaise_api.SuperLachaiseCategory', null=True)),
                ('used_in', models.ManyToManyField(related_name='wikidata_occupations', verbose_name='utilis\xe9 dans', to='superlachaise_api.WikidataEntry', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'wikidata occupation',
                'verbose_name_plural': 'wikidata occupations',
            },
        ),
        migrations.RemoveField(
            model_name='superlachaiseoccupation',
            name='superlachaise_category',
        ),
        migrations.RemoveField(
            model_name='superlachaiseoccupation',
            name='used_in',
        ),
        migrations.DeleteModel(
            name='SuperLachaiseOccupation',
        ),
    ]
