# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0045_auto_20150530_2010'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='openstreetmapelement',
            options={'ordering': ['sorting_name', 'id'], 'verbose_name': '\xe9l\xe9ment OpenStreetMap', 'verbose_name_plural': '\xe9l\xe9ments OpenStreetMap'},
        ),
        migrations.AlterField(
            model_name='pendingmodification',
            name='action',
            field=models.CharField(max_length=255, verbose_name='action', choices=[(b'create', b'create'), (b'modify', b'modify'), (b'delete', b'delete')]),
        ),
    ]
