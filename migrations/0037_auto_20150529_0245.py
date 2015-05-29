# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0036_auto_20150529_0132'),
    ]

    operations = [
        migrations.AddField(
            model_name='wikidataentry',
            name='name',
            field=models.CharField(max_length=255, verbose_name='nom', blank=True),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='instance_of',
            field=models.CharField(max_length=255, verbose_name='nature', blank=True),
        ),
    ]
