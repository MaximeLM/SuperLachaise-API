# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0039_wikidataentry_grave_of_wikidata'),
    ]

    operations = [
        migrations.AddField(
            model_name='wikidataentry',
            name='burial_plot_reference',
            field=models.CharField(max_length=255, verbose_name='num\xe9ro de division', blank=True),
        ),
    ]
