# -*- coding: utf-8 -*-
"""
Settings.
"""

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# Django debug settings.
DEBUG = getattr(settings, 'DEBUG', False)

# Django installed apps
INSTALLED_APPS = settings.INSTALLED_APPS
CACHES = settings.CACHES

# Project path defined in Django settings
PROJECT_PATH = getattr(settings, 'PROJECT_PATH', None)
if PROJECT_PATH is None:
    raise ImproperlyConfigured('PROJECT_PATH must be defined')

# Celery application
CELERY_WORKERS = getattr(settings, 'STATUS_CELERY_WORKERS', ())

# Tuple of application name, provider, args, kwargs
CHECK_PROVIDERS = (
    ('ping', 'status.check_providers.ping', None, None),
    ('code', 'status.check_providers.code', None, None),
    ('databases', 'status.check_providers.databases', None, None),
    ('databases/stats', 'status.check_providers.databases_stats', None, None),
    ('caches', 'status.check_providers.caches', None, None),
)
if CELERY_WORKERS:
    CHECK_PROVIDERS += (
        ('celery', 'status.check_providers.celery', None, {'workers': CELERY_WORKERS}),
        ('celery/stats', 'status.check_providers.celery_stats', None, {'workers': CELERY_WORKERS}),
    )
CHECK_PROVIDERS += getattr(settings, 'STATUS_CHECK_PROVIDERS', ())
