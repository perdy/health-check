# -*- coding: utf-8 -*-
"""
Settings.
"""
import os
from importlib import import_module

__all__ = ['settings']


class Settings:
    debug = False
    base_dir = None
    installed_apps = ()
    caches = {}
    celery_workers = ()
    providers = {'health': (), 'stats': ()}

    def __init__(self):
        module_path = os.environ.get('HEALTH_CHECK_SETTINGS')
        if module_path:
            self.build_from_module(module_path)

    @staticmethod
    def import_settings(path):
        try:
            s = import_module(path)
        except ImportError:
            m, c = path.rsplit('.', 1)
            module = import_module(m)
            s = getattr(module, c)

        return s

    def _add_celery_providers(self):
        self.providers['health'] += (
            ('celery', 'health_check.providers.celery.health.celery', None, {'workers': self.celery_workers}),
        )
        self.providers['stats'] += (
            ('celery', 'health_check.providers.celery.stats.celery', None, {'workers': self.celery_workers}),
        )

    def build_from_module(self, module=None):
        if isinstance(module, str):
            module = self.import_settings(module)

        # Project path defined in settings
        self.base_dir = getattr(module, 'base_dir', None)

        # Celery application
        self.celery_workers = getattr(module, 'health_check_celery_workers', ())

        # Mapping of resources to list of providers
        # Each provider is a tuple of application name, provider, args, kwargs
        self.providers = getattr(module, 'health_check_providers', {
            'health': (
                ('ping', 'health_check.providers.health.ping', None, None),
            ),
            'stats': (
                ('code', 'health_check.providers.stats.code', None, None),
            )
        })

        # If there is celery workers then add celery providers
        if self.celery_workers:
            self._add_celery_providers()

    def build_from_django(self):
        from django.conf import settings as django_settings

        # Django debug settings.
        self.debug = getattr(django_settings, 'DEBUG', False)

        # Django installed apps
        self.installed_apps = getattr(django_settings, 'INSTALLED_APPS', [])
        self.caches = getattr(django_settings, 'CACHES', {})

        # Project path defined in Django settings
        self.base_dir = getattr(django_settings, 'BASE_DIR', None)

        # Celery application
        self.celery_workers = getattr(django_settings, 'HEALTH_CHECK_CELERY_WORKERS', ())

        # Mapping of resources to list of providers
        # Each provider is a tuple of application name, provider, args, kwargs
        self.providers = getattr(django_settings, 'HEALTH_CHECK_PROVIDERS', {
            'health': (
                ('ping', 'health_check.providers.health.ping', None, None),
                ('databases', 'health_check.providers.django.health.databases', None, None),
                ('caches', 'health_check.providers.django.health.caches', None, None),
            ),
            'stats': (
                ('databases', 'health_check.providers.django.stats.databases', None, None),
                ('code', 'health_check.providers.stats.code', None, None),
            )
        })

        # If there is celery workers then add celery providers
        if self.celery_workers:
            self._add_celery_providers()

settings = Settings()
