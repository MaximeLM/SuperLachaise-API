# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pendingmodification',
            name='action',
            field=models.CharField(max_length=255, verbose_name='action', choices=[(b'create_or_update', b'create_or_update'), (b'delete', b'delete')]),
        ),
    ]
