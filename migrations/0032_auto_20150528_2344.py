# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0031_auto_20150528_1956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='openstreetmapelement',
            name='subject_wikidata',
        ),
        migrations.AddField(
            model_name='openstreetmapelement',
            name='subject_wikipedia',
            field=models.CharField(max_length=255, verbose_name='subject:wikipedia', blank=True),
        ),
    ]
