# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0048_auto_20150530_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wikipediapage',
            name='name',
            field=models.CharField(max_length=255, verbose_name='nom'),
        ),
    ]
