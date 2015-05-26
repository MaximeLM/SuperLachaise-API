# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0006_auto_20150526_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivedmodification',
            name='new_values',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='language',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='new_values',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='setting',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
