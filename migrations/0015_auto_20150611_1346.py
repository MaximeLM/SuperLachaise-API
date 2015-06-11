# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0014_auto_20150611_0109'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wikidataoccupation',
            options={'ordering': ['id'], 'verbose_name': 'occupations wikidata', 'verbose_name_plural': 'occupations wikidata'},
        ),
    ]
