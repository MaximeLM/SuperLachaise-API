# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0070_auto_20150602_0140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wikimediacommonsfile',
            name='attribution',
        ),
        migrations.RemoveField(
            model_name='wikimediacommonsfile',
            name='height',
        ),
        migrations.RemoveField(
            model_name='wikimediacommonsfile',
            name='width',
        ),
    ]
