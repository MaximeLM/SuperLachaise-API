# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0032_auto_20150528_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pendingmodification',
            name='action',
            field=models.CharField(max_length=255, verbose_name='action', choices=[(b'create', b'create'), (b'modify', b'modify'), (b'delete', b'delete'), (b'error', b'error')]),
        ),
    ]
