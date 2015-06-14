# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superlachaise_api', '0016_auto_20150614_1951'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalizedAdminCommand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('admin_command', models.ForeignKey(related_name='localizations', verbose_name='commande admin', to='superlachaise_api.AdminCommand')),
                ('language', models.ForeignKey(verbose_name='langage', to='superlachaise_api.Language')),
            ],
            options={
                'ordering': ['language', 'admin_command'],
                'verbose_name': 'localized admin command',
                'verbose_name_plural': 'localized admin commands',
            },
        ),
        migrations.CreateModel(
            name='LocalizedSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='cr\xe9\xe9 le')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modifi\xe9 le')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('language', models.ForeignKey(verbose_name='langage', to='superlachaise_api.Language')),
                ('setting', models.ForeignKey(related_name='localizations', verbose_name='param\xe8tre', to='superlachaise_api.Setting')),
            ],
            options={
                'ordering': ['language', 'setting'],
                'verbose_name': 'localized setting',
                'verbose_name_plural': 'localized settings',
            },
        ),
    ]
