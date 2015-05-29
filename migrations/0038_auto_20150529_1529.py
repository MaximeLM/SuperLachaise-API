# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0037_auto_20150529_0245'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wikidataentry',
            options={'ordering': ['name', 'id'], 'verbose_name': 'entr\xe9e wikidata', 'verbose_name_plural': 'entr\xe9es wikidata'},
        ),
        migrations.AddField(
            model_name='openstreetmapelement',
            name='artist_wikipedia',
            field=models.CharField(max_length=255, verbose_name='artist:wikipedia', blank=True),
        ),
    ]
