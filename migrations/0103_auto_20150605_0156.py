# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0102_auto_20150605_0152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='superlachaisecategory',
            name='values',
            field=models.CharField(max_length=255, verbose_name='codes', blank=True),
        ),
    ]
