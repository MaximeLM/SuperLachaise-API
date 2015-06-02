# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0075_auto_20150602_1750'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='superlachaisepoi',
            options={'verbose_name': 'superlachaise POI', 'verbose_name_plural': 'superlachaise POIs'},
        ),
        migrations.AlterModelOptions(
            name='superlachaisepoiwikidataentryrelation',
            options={'ordering': ['superlachaise_poi', 'type', 'wikidata_entry'], 'verbose_name': 'superlachaise POI wikidata entry relation', 'verbose_name_plural': 'superlachaise POI wikidata entry relations'},
        ),
    ]
