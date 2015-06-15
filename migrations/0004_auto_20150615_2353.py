# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0003_auto_20150615_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wikidatalocalizedentry',
            name='language',
            field=models.ForeignKey(to='superlachaise_api.Language', to_field=b'code', verbose_name='language'),
        ),
        migrations.AlterField(
            model_name='wikidatalocalizedentry',
            name='wikidata_entry',
            field=models.ForeignKey(related_name='localizations', verbose_name='wikidata entry', to_field=b'wikidata_id', to='superlachaise_api.WikidataEntry'),
        ),
    ]
