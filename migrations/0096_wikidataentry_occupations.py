# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0095_superlachaisecategory_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='wikidataentry',
            name='occupations',
            field=models.CharField(max_length=255, verbose_name='occupations', blank=True),
        ),
    ]
