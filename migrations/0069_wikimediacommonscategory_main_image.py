# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0068_auto_20150601_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='wikimediacommonscategory',
            name='main_image',
            field=models.CharField(max_length=255, verbose_name='main image', blank=True),
        ),
    ]
