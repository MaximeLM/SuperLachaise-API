# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0088_openstreetmapelement_nature'),
    ]

    operations = [
        migrations.AddField(
            model_name='wikidataentry',
            name='sex_or_gender',
            field=models.CharField(max_length=255, verbose_name='sex or gender', blank=True),
        ),
    ]
