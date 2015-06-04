# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0092_auto_20150604_2044'),
    ]

    operations = [
        migrations.AddField(
            model_name='superlachaisecategory',
            name='code',
            field=models.CharField(default='code', max_length=255, verbose_name='code'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='superlachaisecategory',
            name='type',
            field=models.CharField(default='type', max_length=255, verbose_name='type'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='superlachaisecategory',
            unique_together=set([('type', 'code')]),
        ),
    ]
