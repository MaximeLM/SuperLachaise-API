# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0085_auto_20150602_1948'),
    ]

    operations = [
        migrations.AddField(
            model_name='wikidatalocalizedentry',
            name='intro',
            field=models.TextField(verbose_name='intro', blank=True),
        ),
    ]
