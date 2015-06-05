# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0098_auto_20150605_0136'),
    ]

    operations = [
        migrations.AddField(
            model_name='superlachaiseoccupation',
            name='used_in_wikidata_entries',
            field=models.IntegerField(default=0, verbose_name='used in wikidata entries'),
        ),
    ]
