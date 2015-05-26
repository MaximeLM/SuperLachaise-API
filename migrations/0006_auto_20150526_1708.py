# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0005_remove_pendingmodification_apply'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='category',
            field=models.CharField(default='default', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='setting',
            unique_together=set([('category', 'key')]),
        ),
    ]
