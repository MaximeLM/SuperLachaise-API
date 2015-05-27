# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0017_auto_20150527_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='id',
            field=models.CharField(max_length=255, serialize=False, verbose_name='id', primary_key=True),
        ),
    ]
