# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0066_auto_20150601_1753'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wikimediacommonsfile',
            name='size',
        ),
        migrations.AddField(
            model_name='wikimediacommonsfile',
            name='height',
            field=models.IntegerField(null=True, verbose_name='height'),
        ),
        migrations.AddField(
            model_name='wikimediacommonsfile',
            name='width',
            field=models.IntegerField(null=True, verbose_name='width'),
        ),
    ]
