# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0013_openstreetmappoi_type'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SyncOperation',
            new_name='AdminCommand',
        ),
    ]
