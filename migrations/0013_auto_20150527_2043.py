# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0012_auto_20150527_2028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='superlachaiseobject',
            name='openStreetMap_element',
        ),
        migrations.RemoveField(
            model_name='wikidataentry',
            name='superlachaise_object',
        ),
        migrations.DeleteModel(
            name='SuperLachaiseObject',
        ),
    ]
