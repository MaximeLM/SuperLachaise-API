# -*- coding: utf-8 -*-

"""
apps.py
superlachaise_api

Created by Maxime Le Moine on 30/05/2015.
Copyright (c) 2015 Maxime Le Moine.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    
    http:www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class SuperLachaiseAPI(AppConfig):
    name = 'superlachaise_api'
    verbose_name = _('SuperLachaise API')
