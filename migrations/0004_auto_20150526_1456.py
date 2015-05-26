# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0003_auto_20150526_0141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivedmodification',
            name='new_values',
            field=models.CharField(max_length=2000, blank=True),
        ),
    ]
