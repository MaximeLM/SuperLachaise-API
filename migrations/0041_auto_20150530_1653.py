# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0040_wikidataentry_burial_plot_reference'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='openstreetmapelement',
            name='artist_wikipedia',
        ),
        migrations.RemoveField(
            model_name='openstreetmapelement',
            name='subject_wikipedia',
        ),
        migrations.AddField(
            model_name='openstreetmapelement',
            name='wikidata_combined',
            field=models.CharField(max_length=255, verbose_name='wikidata_combined', blank=True),
        ),
    ]
