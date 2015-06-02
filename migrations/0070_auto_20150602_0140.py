# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0069_wikimediacommonscategory_main_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wikimediacommonsfile',
            name='original_url',
            field=models.CharField(max_length=500, verbose_name='url original', blank=True),
        ),
        migrations.AlterField(
            model_name='wikimediacommonsfile',
            name='thumbnail_template_url',
            field=models.CharField(max_length=500, verbose_name='mod\xe8le url vignette', blank=True),
        ),
    ]
