# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0038_auto_20150529_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='wikidataentry',
            name='grave_of_wikidata',
            field=models.CharField(max_length=255, verbose_name='grave_of:wikidata', blank=True),
        ),
    ]
