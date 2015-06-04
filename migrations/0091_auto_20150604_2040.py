# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0090_auto_20150604_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='superlachaisewikidatarelation',
            name='relation_type',
            field=models.CharField(max_length=255, verbose_name='relation type'),
        ),
    ]
