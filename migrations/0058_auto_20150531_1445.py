# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0057_auto_20150531_0227'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='wikipediapage',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='wikipediapage',
            name='language',
        ),
        migrations.DeleteModel(
            name='WikipediaPage',
        ),
    ]
