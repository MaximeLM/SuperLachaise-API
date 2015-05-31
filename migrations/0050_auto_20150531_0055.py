# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0049_auto_20150530_2123'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wikipediapage',
            options={'ordering': ['name', 'language'], 'verbose_name': 'page wikip\xe9dia', 'verbose_name_plural': 'pages wikip\xe9dia'},
        ),
        migrations.AddField(
            model_name='wikipediapage',
            name='revision_id',
            field=models.CharField(default='', max_length=255, verbose_name='revision id'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='wikipediapage',
            name='date_of_birth_accuracy',
            field=models.CharField(blank=True, max_length=255, verbose_name='pr\xe9cision date de naissance', choices=[(b'Year', 'Ann\xe9e'), (b'Month', 'Mois'), (b'Day', 'Jour')]),
        ),
        migrations.AlterField(
            model_name='wikipediapage',
            name='date_of_death_accuracy',
            field=models.CharField(blank=True, max_length=255, verbose_name='pr\xe9cision date de d\xe9c\xe8s', choices=[(b'Year', 'Ann\xe9e'), (b'Month', 'Mois'), (b'Day', 'Jour')]),
        ),
    ]
