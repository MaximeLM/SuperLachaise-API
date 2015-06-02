# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0082_auto_20150602_1909'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='superlachaisewikidatarelation',
            options={'ordering': ['superlachaise_poi', 'relation_type', 'wikidata_entry'], 'verbose_name': 'superlachaisepoi-wikidataentry relationship', 'verbose_name_plural': 'superlachaisepoi-wikidataentry relationships'},
        ),
    ]
