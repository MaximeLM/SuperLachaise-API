# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0087_auto_20150602_2031'),
    ]

    operations = [
        migrations.AddField(
            model_name='openstreetmapelement',
            name='nature',
            field=models.CharField(max_length=255, verbose_name='nature', blank=True),
        ),
    ]
