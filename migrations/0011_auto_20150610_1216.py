# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0010_superlachaiselocalizedpoi_sorting_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wikipediapage',
            options={'ordering': ['default_sort', 'wikidata_localized_entry'], 'verbose_name': 'page wikip\xe9dia', 'verbose_name_plural': 'pages wikip\xe9dia'},
        ),
        migrations.AlterField(
            model_name='superlachaiselocalizedpoi',
            name='sorting_name',
            field=models.CharField(max_length=255, verbose_name='nom pour tri', blank=True),
        ),
    ]
