# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0094_auto_20150604_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='superlachaisecategory',
            name='name',
            field=models.CharField(default='name', unique=True, max_length=255, verbose_name='name'),
            preserve_default=False,
        ),
    ]
