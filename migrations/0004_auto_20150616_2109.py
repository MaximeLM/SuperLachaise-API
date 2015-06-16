# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0003_auto_20150616_1942'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenStreetMapWikiPediaTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('prefix', models.CharField(max_length=255, verbose_name='prefix', blank=True)),
                ('language_code', models.CharField(max_length=255, verbose_name='language code', blank=True)),
                ('wikipedia', models.CharField(max_length=255, verbose_name='wikipedia', blank=True)),
                ('wikipedia_of', models.ForeignKey(related_name='wiki_tags', verbose_name='wikipedia_of', to='superlachaise_api.OpenStreetMapElement')),
            ],
            options={
                'ordering': ['prefix', 'language_code', 'wikipedia'],
                'verbose_name': 'openstreetmap wikipedia tag',
                'verbose_name_plural': 'openstreetmap wikipedia tags',
            },
        ),
        migrations.AlterUniqueTogether(
            name='openstreetmapwikipediatag',
            unique_together=set([('prefix', 'language_code', 'wikipedia')]),
        ),
    ]
