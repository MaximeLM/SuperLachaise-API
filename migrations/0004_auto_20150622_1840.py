# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0003_auto_20150621_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='latitude',
            field=models.DecimalField(default=0, verbose_name='latitude', max_digits=10, decimal_places=7),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='longitude',
            field=models.DecimalField(default=0, verbose_name='longitude', max_digits=10, decimal_places=7),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='openstreetmapelement',
            name='type',
            field=models.CharField(db_index=True, max_length=255, verbose_name='type', choices=[(b'node', b'node'), (b'way', b'way'), (b'relation', b'relation')]),
        ),
    ]
