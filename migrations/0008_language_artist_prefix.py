# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0007_remove_setting_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='artist_prefix',
            field=models.CharField(default='skdfg', max_length=255, verbose_name='artist prefix'),
            preserve_default=False,
        ),
    ]
