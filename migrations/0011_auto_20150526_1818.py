# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0010_auto_20150526_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='syncoperation',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
