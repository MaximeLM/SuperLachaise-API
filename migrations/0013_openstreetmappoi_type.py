# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0012_remove_syncoperation_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='openstreetmappoi',
            name='type',
            field=models.CharField(default='node', max_length=255, choices=[(b'node', b'node'), (b'way', b'way'), (b'relation', b'relation')]),
            preserve_default=False,
        ),
    ]
