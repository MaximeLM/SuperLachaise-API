# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0026_auto_20150528_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='wikidataentry',
            name='wikimedia_commons_grave',
            field=models.CharField(max_length=255, verbose_name='wikimedia commons grave', blank=True),
        ),
    ]
