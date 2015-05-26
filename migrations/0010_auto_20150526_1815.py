# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0009_syncoperation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='syncoperation',
            name='status',
            field=models.CharField(default=b'not_executed', max_length=255, choices=[(b'not_executed', 'not executed'), (b'running', b'running'), (b'finished', b'finished')]),
        ),
    ]
