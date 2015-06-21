# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0001_squashed_0002_auto_20150619_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='openstreetmap_id',
            field=models.CharField(max_length=255, verbose_name='openstreetmap id', db_index=True),
        ),
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='type',
            field=models.CharField(blank=True, max_length=255, verbose_name='type', db_index=True, choices=[(b'node', b'node'), (b'way', b'way'), (b'relation', b'relation')]),
        ),
        migrations.AlterUniqueTogether(
            name='openstreetmapelement',
            unique_together=set([('type', 'openstreetmap_id')]),
        ),
    ]
