# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0012_auto_20150610_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admincommand',
            name='dependency_order',
            field=models.IntegerField(null=True, verbose_name='ordre de d\xe9pendance', blank=True),
        ),
        migrations.AlterField(
            model_name='wikipediapage',
            name='default_sort',
            field=models.CharField(max_length=255, verbose_name='tri par d\xe9faut', blank=True),
        ),
    ]
