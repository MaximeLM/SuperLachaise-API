# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0065_auto_20150601_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='wikimediacommonsfile',
            name='size',
            field=models.CharField(max_length=255, verbose_name='dimensions', blank=True),
        ),
        migrations.AlterField(
            model_name='wikimediacommonsfile',
            name='url_original',
            field=models.CharField(max_length=255, verbose_name='url original', blank=True),
        ),
        migrations.AlterField(
            model_name='wikimediacommonsfile',
            name='url_thumbnail',
            field=models.CharField(max_length=255, verbose_name='url vignette', blank=True),
        ),
    ]
