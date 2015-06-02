# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0081_auto_20150602_1844'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='superlachaisewikidatarelation',
            options={'ordering': ['superlachaise_poi', 'relation_type', 'wikidata_entry'], 'verbose_name': 'wikidata entry', 'verbose_name_plural': 'wikidata entries'},
        ),
        migrations.RemoveField(
            model_name='superlachaisewikidatarelation',
            name='type',
        ),
        migrations.AddField(
            model_name='superlachaisewikidatarelation',
            name='relation_type',
            field=models.CharField(max_length=255, verbose_name='relation type', blank=True),
        ),
    ]
