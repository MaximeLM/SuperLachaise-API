# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0024_auto_20150528_0231'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalizedWikidataEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('name', models.CharField(max_length=255, verbose_name='nom', blank=True)),
                ('wikipedia', models.CharField(max_length=255, verbose_name='wikip\xe9dia', blank=True)),
                ('description', models.CharField(max_length=255, verbose_name='description', blank=True)),
                ('language', models.ForeignKey(to='superlachaise_api.Language')),
                ('parent', models.ForeignKey(to='superlachaise_api.WikidataEntry')),
            ],
            options={
                'verbose_name': 'localized wikidata entry',
                'verbose_name_plural': 'localized wikidata entries',
            },
        ),
        migrations.AlterUniqueTogether(
            name='wikidatalocalizedentry',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='wikidatalocalizedentry',
            name='language',
        ),
        migrations.RemoveField(
            model_name='wikidatalocalizedentry',
            name='parent',
        ),
        migrations.DeleteModel(
            name='WikidataLocalizedEntry',
        ),
        migrations.AlterUniqueTogether(
            name='localizedwikidataentry',
            unique_together=set([('parent', 'language')]),
        ),
    ]
