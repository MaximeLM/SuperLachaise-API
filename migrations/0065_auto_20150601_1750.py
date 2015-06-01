# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0064_auto_20150601_1710'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wikimediacommonsfile',
            name='url',
        ),
        migrations.AddField(
            model_name='wikimediacommonsfile',
            name='url_original',
            field=models.CharField(max_length=255, verbose_name='original url', blank=True),
        ),
        migrations.AddField(
            model_name='wikimediacommonsfile',
            name='url_thumbnail',
            field=models.CharField(max_length=255, verbose_name='thumbnail url', blank=True),
        ),
    ]
