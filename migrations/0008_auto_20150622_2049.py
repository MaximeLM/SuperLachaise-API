# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0007_delete_deletedobject'),
    ]

    operations = [
        migrations.AddField(
            model_name='openstreetmapelement',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='deleted'),
        ),
        migrations.AddField(
            model_name='superlachaisecategory',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='deleted'),
        ),
        migrations.AddField(
            model_name='superlachaisepoi',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='deleted'),
        ),
        migrations.AddField(
            model_name='wikidataentry',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='deleted'),
        ),
        migrations.AddField(
            model_name='wikimediacommonscategory',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='deleted'),
        ),
    ]
