# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0097_superlachaiseoccupation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='superlachaiseoccupation',
            name='superlachaise_category',
            field=models.ForeignKey(related_name='occupations', verbose_name='superlachaise category', blank=True, to='superlachaise_api.SuperLachaiseCategory'),
        ),
    ]
