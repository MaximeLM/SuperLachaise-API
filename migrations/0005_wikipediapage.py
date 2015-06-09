# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0004_auto_20150609_1610'),
    ]

    operations = [
        migrations.CreateModel(
            name='WikipediaPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('intro', models.TextField(verbose_name='intro', blank=True)),
                ('wikidata_localized_entry', models.OneToOneField(related_name='wikipedia_page', verbose_name='entr\xe9e wikidata localis\xe9e', to='superlachaise_api.WikidataLocalizedEntry')),
            ],
            options={
                'ordering': ['wikidata_localized_entry'],
                'verbose_name': 'wikipedia page',
                'verbose_name_plural': 'wikipedia pages',
            },
        ),
    ]
