# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0011_auto_20150623_0557'),
    ]

    operations = [
        migrations.AddField(
            model_name='wikimediacommonscategory',
            name='category_members',
            field=models.TextField(verbose_name='category members', blank=True),
        ),
        migrations.AlterField(
            model_name='superlachaisepoi',
            name='openstreetmap_element',
            field=models.OneToOneField(related_name='superlachaise_poi', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='superlachaise_api.OpenStreetMapElement', verbose_name='openstreetmap element'),
        ),
    ]
