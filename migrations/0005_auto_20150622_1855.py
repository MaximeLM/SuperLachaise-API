# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0004_auto_20150622_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='latitude',
            field=models.DecimalField(default=0, verbose_name='latitude', max_digits=10, decimal_places=7),
        ),
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='longitude',
            field=models.DecimalField(default=0, verbose_name='longitude', max_digits=10, decimal_places=7),
        ),
    ]
