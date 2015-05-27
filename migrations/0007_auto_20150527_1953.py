# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0006_auto_20150527_1945'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('code', models.CharField(unique=True, max_length=10, verbose_name='code')),
                ('description', models.CharField(max_length=255, verbose_name='description', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WikidataLocalizedEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('name', models.CharField(max_length=255, verbose_name='nom')),
                ('wikipedia', models.CharField(max_length=255, verbose_name='wikip\xe9dia', blank=True)),
                ('description', models.CharField(max_length=255, verbose_name='description', blank=True)),
                ('wikipedia_intro', models.TextField(verbose_name='wikipedia intro', blank=True)),
                ('language', models.ForeignKey(to='superlachaise_api.Language')),
            ],
            options={
                'verbose_name': 'wikidata localized entry',
                'verbose_name_plural': 'wikidata localized entries',
            },
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='date_of_birth_accuracy',
            field=models.CharField(max_length=1, choices=[(b'Y', 'Year'), (b'M', 'Month'), (b'D', 'Day')]),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='date_of_death_accuracy',
            field=models.CharField(max_length=1, choices=[(b'Y', 'Year'), (b'M', 'Month'), (b'D', 'Day')]),
        ),
        migrations.AddField(
            model_name='wikidatalocalizedentry',
            name='wikidata_entry',
            field=models.ForeignKey(to='superlachaise_api.WikidataEntry'),
        ),
    ]
