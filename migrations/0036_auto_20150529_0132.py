# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0035_auto_20150529_0120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wikidataentry',
            name='is_a_person',
        ),
        migrations.AddField(
            model_name='wikidataentry',
            name='instance_of',
            field=models.CharField(max_length=255, verbose_name='instance of', blank=True),
        ),
    ]
