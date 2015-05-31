# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0055_auto_20150531_0226'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wikipediapage',
            old_name='last_revision_idd',
            new_name='last_revision_id',
        ),
    ]
