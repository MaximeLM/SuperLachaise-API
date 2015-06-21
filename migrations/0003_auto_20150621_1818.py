# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0002_auto_20150621_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='superlachaisepoi',
            name='burial_plot_reference',
            field=models.CharField(max_length=255, verbose_name='burial plot reference', blank=True),
        ),
        migrations.AddField(
            model_name='superlachaisepoi',
            name='date_of_birth',
            field=models.DateField(null=True, verbose_name='date of birth', blank=True),
        ),
        migrations.AddField(
            model_name='superlachaisepoi',
            name='date_of_birth_accuracy',
            field=models.CharField(blank=True, max_length=255, verbose_name='date of birth accuracy', choices=[(b'Year', 'Year'), (b'Month', 'Month'), (b'Day', 'Day')]),
        ),
        migrations.AddField(
            model_name='superlachaisepoi',
            name='date_of_death',
            field=models.DateField(null=True, verbose_name='date of death', blank=True),
        ),
        migrations.AddField(
            model_name='superlachaisepoi',
            name='date_of_death_accuracy',
            field=models.CharField(blank=True, max_length=255, verbose_name='date of death accuracy', choices=[(b'Year', 'Year'), (b'Month', 'Month'), (b'Day', 'Day')]),
        ),
    ]
