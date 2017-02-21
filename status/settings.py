# -*- coding: utf-8 -*-
"""
Settings.
"""
__all__ = ['settings']


class Settings:
    debug = False
    base_dir = None
    installed_apps = ()
    caches = {}
    celery_workers = ()
    providers = {'health': (), 'stats': ()}

    @classmethod
    def _add_celery_providers(cls):
        cls.providers['health'] += (
            ('celery', 'status.providers.celery.health.celery', None, {'workers': cls.celery_workers}),
        )
        cls.providers['stats'] += (
            ('celery', 'status.providers.celery.stats.celery', None, {'workers': cls.celery_workers}),
        )

    @classmethod
    def build_from_module(cls, module=None):
        # Project path defined in settings
        cls.base_dir = getattr(module, 'BASE_DIR', None)

        # Celery application
        cls.celery_workers = getattr(module, 'STATUS_CELERY_WORKERS', ())

        # Mapping of resources to list of providers
        # Each provider is a tuple of application name, provider, args, kwargs
        cls.providers = getattr(module, 'STATUS_PROVIDERS', {
            'health': (
                ('ping', 'status.providers.health.ping', None, None),
            ),
            'stats': (
                ('code', 'status.providers.stats.code', None, None),
            )
        })

        # If there is celery workers then add celery providers
        if cls.celery_workers:
            cls._add_celery_providers()

    @classmethod
    def build_from_django(cls):
        from django.conf import settings as django_settings

        # Django debug settings.
        cls.debug = getattr(django_settings, 'DEBUG', False)

        # Django installed apps
        cls.installed_apps = getattr(django_settings, 'INSTALLED_APPS', [])
        cls.caches = getattr(django_settings, 'CACHES', {})

        # Project path defined in Django settings
        cls.base_dir = getattr(django_settings, 'BASE_DIR', None)

        # Celery application
        cls.celery_workers = getattr(django_settings, 'STATUS_CELERY_WORKERS', ())

        # Mapping of resources to list of providers
        # Each provider is a tuple of application name, provider, args, kwargs
        cls.providers = getattr(django_settings, 'STATUS_PROVIDERS', {
            'health': (
                ('ping', 'status.providers.health.ping', None, None),
                ('databases', 'status.providers.django.health.databases', None, None),
                ('caches', 'status.providers.django.health.caches', None, None),
            ),
            'stats': (
                ('databases', 'status.providers.django.stats.databases', None, None),
                ('code', 'status.providers.stats.code', None, None),
            )
        })

        # If there is celery workers then add celery providers
        if cls.celery_workers:
            cls._add_celery_providers()

settings = Settings()
