# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0015_auto_20150611_1346'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='superlachaiselocalizedcategory',
            unique_together=set([('superlachaise_category', 'language')]),
        ),
    ]
