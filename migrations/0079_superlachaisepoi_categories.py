# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0078_auto_20150602_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='superlachaisepoi',
            name='categories',
            field=models.ManyToManyField(related_name='superlachaise_pois', verbose_name='categories', to='superlachaise_api.SuperLachaiseCategory'),
        ),
    ]
