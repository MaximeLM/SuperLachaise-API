# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0083_auto_20150602_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wikidatalocalizedentry',
            name='wikidata_entry',
            field=models.ForeignKey(related_name='localizations', verbose_name='wikidata entry', to='superlachaise_api.WikidataEntry'),
        ),
    ]
