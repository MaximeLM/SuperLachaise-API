# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0027_wikidataentry_wikimedia_commons_grave'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wikidataentry',
            name='wikimedia_commons',
        ),
        migrations.RemoveField(
            model_name='wikidataentry',
            name='wikimedia_commons_grave',
        ),
        migrations.AddField(
            model_name='wikidataentry',
            name='wikimedia_commons_category',
            field=models.CharField(max_length=255, verbose_name='wikimedia commons category', blank=True),
        ),
        migrations.AddField(
            model_name='wikidataentry',
            name='wikimedia_commons_grave_category',
            field=models.CharField(max_length=255, verbose_name='wikimedia commons grave category', blank=True),
        ),
    ]
