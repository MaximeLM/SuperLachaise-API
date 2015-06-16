# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0006_auto_20150616_2114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='openstreetmapelement',
            name='wikidata_combined',
        ),
        migrations.RemoveField(
            model_name='openstreetmapelement',
            name='wikipedia',
        ),
    ]
