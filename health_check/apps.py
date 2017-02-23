# -*- coding: utf-8 -*-
"""Django application config module.
"""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from health_check.settings import settings


class HealthCheck(AppConfig):
    name = 'health_check'
    verbose_name = _('Health Check')

    def ready(self):
        settings.build_from_django()
