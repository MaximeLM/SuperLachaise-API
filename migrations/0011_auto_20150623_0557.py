# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0010_wikipediapage_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='superlachaisepoi',
            name='openstreetmap_element',
            field=models.OneToOneField(related_name='superlachaise_poi', null=True, on_delete=django.db.models.deletion.SET_NULL, verbose_name='openstreetmap element', to='superlachaise_api.OpenStreetMapElement'),
        ),
    ]
