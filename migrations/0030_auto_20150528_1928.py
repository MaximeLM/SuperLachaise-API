# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0029_auto_20150528_1522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='openstreetmapelement',
            name='historic',
        ),
        migrations.AddField(
            model_name='openstreetmapelement',
            name='name_wikidata',
            field=models.CharField(max_length=255, verbose_name='name:wikidata', blank=True),
        ),
    ]
