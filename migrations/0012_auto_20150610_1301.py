# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0011_auto_20150610_1216'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='superlachaiselocalizedpoi',
            options={'ordering': ['language', 'sorting_name', 'name'], 'verbose_name': 'POI SuperLachaise localis\xe9', 'verbose_name_plural': 'POIs SuperLachaise localis\xe9s'},
        ),
    ]
