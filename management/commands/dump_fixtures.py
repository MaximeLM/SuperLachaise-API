# -*- coding: utf-8 -*-

import os
from django.core.management.base import BaseCommand, CommandError
from django.core import serializers

from superlachaise_api.models import Setting, Language, AdminCommand

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        f = open(os.path.dirname(os.path.realpath(__file__)) + '/../../fixtures/settings.json', "w")
        data = serializers.serialize("json", Setting.objects.all())
        f.write(data)
        f.close()
        
        f = open(os.path.dirname(os.path.realpath(__file__)) + '/../../fixtures/languages.json', "w")
        data = serializers.serialize("json", Language.objects.all())
        f.write(data)
        f.close()
        
        f = open(os.path.dirname(os.path.realpath(__file__)) + '/../../fixtures/admin_commands.json', "w")
        data = serializers.serialize("json", AdminCommand.objects.all())
        f.write(data)
        f.close()
