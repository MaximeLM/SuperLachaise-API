# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0018_auto_20150527_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pendingmodification',
            name='target_object_id',
            field=models.CharField(max_length=255, verbose_name="id de l'objet cible"),
        ),
    ]
