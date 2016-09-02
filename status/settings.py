# -*- coding: utf-8 -*-
"""
Settings.
"""

from django.conf import settings

# Django debug settings.
DEBUG = getattr(settings, 'DEBUG', False)

# Django installed apps
INSTALLED_APPS = settings.INSTALLED_APPS
CACHES = settings.CACHES

# Project path defined in Django settings
BASE_DIR = getattr(settings, 'BASE_DIR', None)

# Celery application
CELERY_WORKERS = getattr(settings, 'STATUS_CELERY_WORKERS', ())

# Mapping of resources to list of providers
# Each provider is a tuple of application name, provider, args, kwargs
PROVIDERS = getattr(settings, 'STATUS_PROVIDERS', {
    'health': (
        ('ping', 'status.providers.health.ping', None, None),
        ('databases', 'status.providers.health.databases', None, None),
        ('caches', 'status.providers.health.caches', None, None),
    ),
    'stats': (
        ('databases', 'status.providers.stats.databases', None, None),
        ('code', 'status.providers.stats.code', None, None),
    )
})

if CELERY_WORKERS:
    PROVIDERS['health'] += (
        ('celery', 'status.providers.health.celery', None, {'workers': CELERY_WORKERS}),
    )
    PROVIDERS['stats'] += (
        ('celery', 'status.providers.stats.celery', None, {'workers': CELERY_WORKERS}),
    )
