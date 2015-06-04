# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0091_auto_20150604_2040'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='superlachaisewikidatarelation',
            unique_together=set([('superlachaise_poi', 'wikidata_entry', 'relation_type')]),
        ),
    ]
