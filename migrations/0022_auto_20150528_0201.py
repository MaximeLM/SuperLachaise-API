# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0021_auto_20150528_0112'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='default_for_display',
            field=models.BooleanField(default=False, verbose_name='default for display'),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='date_of_birth',
            field=models.DateField(null=True, verbose_name='date de naissance', blank=True),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='date_of_birth_accuracy',
            field=models.CharField(blank=True, max_length=1, verbose_name='pr\xe9cision date de naissance', choices=[(b'Y', 'Ann\xe9e'), (b'M', 'Mois'), (b'D', 'Jour')]),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='date_of_death',
            field=models.DateField(null=True, verbose_name='date de d\xe9c\xe8s', blank=True),
        ),
        migrations.AlterField(
            model_name='wikidataentry',
            name='date_of_death_accuracy',
            field=models.CharField(blank=True, max_length=1, verbose_name='pr\xe9cision date de d\xe9c\xe8s', choices=[(b'Y', 'Ann\xe9e'), (b'M', 'Mois'), (b'D', 'Jour')]),
        ),
    ]
