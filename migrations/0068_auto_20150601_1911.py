# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0067_auto_20150601_1755'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wikimediacommonsfile',
            old_name='url_original',
            new_name='original_url',
        ),
        migrations.RemoveField(
            model_name='wikimediacommonsfile',
            name='url_thumbnail',
        ),
        migrations.AddField(
            model_name='wikimediacommonsfile',
            name='thumbnail_template_url',
            field=models.CharField(max_length=255, verbose_name='mod\xe8le url vignette', blank=True),
        ),
        migrations.AlterField(
            model_name='wikimediacommonsfile',
            name='height',
            field=models.IntegerField(null=True, verbose_name='hauteur'),
        ),
        migrations.AlterField(
            model_name='wikimediacommonsfile',
            name='width',
            field=models.IntegerField(null=True, verbose_name='largeur'),
        ),
    ]
