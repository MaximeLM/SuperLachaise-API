# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0011_auto_20150527_2026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wikidataentry',
            name='openStreetMap_element',
        ),
        migrations.AddField(
            model_name='wikidataentry',
            name='superlachaise_object',
            field=models.ForeignKey(default=None, to='superlachaise_api.SuperLachaiseObject'),
            preserve_default=False,
        ),
    ]
