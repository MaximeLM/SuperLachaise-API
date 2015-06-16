# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0005_auto_20150616_2112'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='openstreetmapwikipediatag',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='openstreetmapwikipediatag',
            name='wikipedia_of',
        ),
        migrations.DeleteModel(
            name='OpenStreetMapWikiPediaTag',
        ),
    ]
