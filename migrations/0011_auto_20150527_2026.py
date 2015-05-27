# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0010_auto_20150527_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='superlachaiseobject',
            name='openStreetMap_element',
            field=models.OneToOneField(verbose_name='openstreetmap element', to='superlachaise_api.OpenStreetMapElement'),
        ),
    ]
