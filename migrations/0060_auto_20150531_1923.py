# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0059_auto_20150531_1446'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wikipediapage',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='wikipediapage',
            name='date_of_birth_accuracy',
        ),
        migrations.RemoveField(
            model_name='wikipediapage',
            name='date_of_death',
        ),
        migrations.RemoveField(
            model_name='wikipediapage',
            name='date_of_death_accuracy',
        ),
    ]
