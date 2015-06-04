# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0093_auto_20150604_2105'),
    ]

    operations = [
        migrations.AddField(
            model_name='superlachaisecategory',
            name='key',
            field=models.CharField(default='key', max_length=255, verbose_name='key'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='superlachaisecategory',
            name='values',
            field=models.CharField(default='values', max_length=255, verbose_name='codes'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='superlachaisecategory',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='superlachaisecategory',
            name='code',
        ),
        migrations.RemoveField(
            model_name='superlachaisecategory',
            name='type',
        ),
    ]
