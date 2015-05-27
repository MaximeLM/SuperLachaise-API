# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0005_auto_20150527_1943'),
    ]

    operations = [
        migrations.CreateModel(
            name='WikidataEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('wikidata', models.CharField(unique=True, max_length=255, verbose_name='wikidata')),
                ('type', models.CharField(max_length=255, verbose_name='type', choices=[(b'place', 'place'), (b'person', 'person'), (b'artist', 'artist'), (b'subject', 'subject')])),
                ('wikimedia_commons', models.CharField(max_length=255, verbose_name='wikimedia commons', blank=True)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('date_of_death', models.DateField(null=True, blank=True)),
                ('date_of_birth_accuracy', models.CharField(default=b'D', max_length=1, choices=[(b'Y', 'Year'), (b'M', 'Month'), (b'D', 'Day')])),
                ('date_of_death_accuracy', models.CharField(default=b'D', max_length=1, choices=[(b'Y', 'Year'), (b'M', 'Month'), (b'D', 'Day')])),
                ('openStreetMap_element', models.ForeignKey(to='superlachaise_api.OpenStreetMapElement')),
            ],
            options={
                'verbose_name': 'wikidata entry',
                'verbose_name_plural': 'wikidata entries',
            },
        ),
        migrations.RemoveField(
            model_name='wikientry',
            name='openStreetMap_element',
        ),
        migrations.DeleteModel(
            name='WikiEntry',
        ),
    ]
