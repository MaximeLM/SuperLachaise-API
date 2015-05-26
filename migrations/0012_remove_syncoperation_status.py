# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0011_auto_20150526_1818'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='syncoperation',
            name='status',
        ),
    ]
