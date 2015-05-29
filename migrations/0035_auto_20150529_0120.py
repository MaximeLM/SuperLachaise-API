# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0034_auto_20150529_0115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wikidataentry',
            name='is_a_person',
            field=models.BooleanField(verbose_name='humain'),
        ),
    ]
