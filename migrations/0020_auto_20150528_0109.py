# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0019_auto_20150527_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wikidataentry',
            name='date_of_birth_accuracy',
            field=models.CharField(max_length=1, null=True, choices=[(b'Y', 'Ann\xe9e'), (b'M', 'Mois'), (b'D', 'Jour')]),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='date_of_death_accuracy',
            field=models.CharField(max_length=1, null=True, choices=[(b'Y', 'Ann\xe9e'), (b'M', 'Mois'), (b'D', 'Jour')]),
        ),
    ]
