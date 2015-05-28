# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0030_auto_20150528_1928'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='openstreetmapelement',
            name='name_wikidata',
        ),
        migrations.AddField(
            model_name='openstreetmapelement',
            name='subject_wikidata',
            field=models.CharField(max_length=255, verbose_name='subject:wikidata', blank=True),
        ),
    ]
