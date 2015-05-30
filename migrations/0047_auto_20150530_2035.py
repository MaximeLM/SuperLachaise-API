# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0046_auto_20150530_2030'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='localizedwikidataentry',
            options={'ordering': ['name', 'language'], 'verbose_name': 'entr\xe9e wikidata localis\xe9e', 'verbose_name_plural': 'entr\xe9es wikidata localis\xe9es'},
        ),
    ]
