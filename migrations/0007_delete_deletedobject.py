# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0006_auto_20150622_1902'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DeletedObject',
        ),
    ]
