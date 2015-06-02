# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0076_auto_20150602_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='superlachaisepoi',
            name='main_image',
            field=models.ForeignKey(related_name='superlachaise_pois', verbose_name='main image', blank=True, to='superlachaise_api.WikimediaCommonsFile', null=True),
        ),
        migrations.AlterField(
            model_name='superlachaisepoi',
            name='wikimedia_commons_category',
            field=models.ForeignKey(related_name='superlachaise_pois', verbose_name='wikimedia commons category', blank=True, to='superlachaise_api.WikimediaCommonsCategory', null=True),
        ),
    ]
