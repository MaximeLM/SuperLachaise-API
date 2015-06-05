# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0104_auto_20150605_0236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='superlachaiseoccupation',
            name='used_in_wikidata_entries',
        ),
        migrations.AddField(
            model_name='superlachaiseoccupation',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name', blank=True),
        ),
        migrations.AddField(
            model_name='superlachaiseoccupation',
            name='used_in',
            field=models.ManyToManyField(related_name='superlachaise_occupations', verbose_name='used in', to='superlachaise_api.WikidataEntry', blank=True),
        ),
    ]
