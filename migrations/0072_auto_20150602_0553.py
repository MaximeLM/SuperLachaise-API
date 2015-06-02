# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0071_auto_20150602_0204'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wikimediacommonsfile',
            name='thumbnail_template_url',
        ),
        migrations.AddField(
            model_name='wikimediacommonsfile',
            name='thumbnail_url',
            field=models.CharField(max_length=500, verbose_name='url vignette', blank=True),
        ),
        migrations.AlterField(
            model_name='wikimediacommonscategory',
            name='main_image',
            field=models.CharField(max_length=255, verbose_name='image principale', blank=True),
        ),
    ]
