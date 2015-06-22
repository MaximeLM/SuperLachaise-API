# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0008_auto_20150622_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='superlachaiselocalizedpoi',
            name='sorting_name',
            field=models.CharField(max_length=255, verbose_name='sorting name'),
        ),
    ]
