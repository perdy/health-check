# -*- coding: utf-8 -*-
"""Django application config module.
"""

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Status(AppConfig):
    name = 'status'
    verbose_name = _('Status')
