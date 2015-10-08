# -*- coding: utf-8 -*-
"""
Module description
"""

try:
    from django.conf import settings
    DEBUG = settings.DEBUG
except (ImportError, AttributeError):
    settings = None

# Celery application
CELERY_APP = getattr(settings, 'STATUS_CELERY_APP', None)

# Tuple of application name, provider, args, kwargs
CHECK_PROVIDERS = (
    ('ping', 'status.check_providers.ping', None, None),
)
if CELERY_APP:
    CHECK_PROVIDERS += (('celery', 'status.check_providers.celery', None, {'app': CELERY_APP}), )
CHECK_PROVIDERS += getattr(settings, 'STATUS_CHECK_PROVIDERS', ())
