# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0022_auto_20150528_0201'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='language',
            name='default_for_display',
        ),
    ]
