# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0020_auto_20150528_0109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wikidataentry',
            name='date_of_birth_accuracy',
            field=models.CharField(default='', max_length=1, blank=True, choices=[(b'Y', 'Ann\xe9e'), (b'M', 'Mois'), (b'D', 'Jour')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='date_of_death_accuracy',
            field=models.CharField(default='', max_length=1, blank=True, choices=[(b'Y', 'Ann\xe9e'), (b'M', 'Mois'), (b'D', 'Jour')]),
            preserve_default=False,
        ),
    ]
