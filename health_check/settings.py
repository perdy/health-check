# -*- coding: utf-8 -*-
"""
Settings.
"""
import os
from functools import partial
from functools import update_wrapper
from importlib import import_module

__all__ = ['settings']


class reset:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        update_wrapper(self, func)

    def __get__(self, instance, owner=None):
        self.instance = instance
        return partial(self, instance)

    def __call__(self, *args, **kwargs):
        self.instance.reset_default()
        self.func(*args, **kwargs)


class Settings:
    debug = False
    base_dir = None
    installed_apps = ()
    caches = {}
    celery_workers = ()
    providers = {'health': (), 'stats': ()}

    def __init__(self):
        self.reset_default()
        module_path = os.environ.get('HEALTH_CHECK_SETTINGS')
        if module_path:
            self.build_from_module(module_path)

    def reset_default(self):
        """
        Reset settings to default values.
        """
        self.debug = False
        self.base_dir = None
        self.installed_apps = ()
        self.caches = {}
        self.celery_workers = ()
        self.providers = {
            'health': (
                ('ping', 'health_check.providers.health.ping', None, None),
            ),
            'stats': (
                ('code', 'health_check.providers.stats.code', None, None),
            )
        }

    @staticmethod
    def import_settings(path):
        """
        Import a settings module that can be a module or an object.
        To import a module, his full path should be specified: *package.settings*.
        To import an object, his full path and object name should be specified: *project.settings:SettingsObject*.

        :param path: Settings full path.
        :return: Settings module or object.
        """
        try:
            try:
                m, c = path.rsplit(':', 1)
                module = import_module(m)
                s = getattr(module, c)
            except ValueError:
                s = import_module(path)
        except ImportError:
            raise ImportError("Settings not found '{}'".format(path))

        return s

    @staticmethod
    def get(s, key, default=None):
        """
        Get a settings value from key. Try to get key as it is, transforming to lower case and to upper case. If not
        found, a default value will be returned.

        :param s: Settings module or object.
        :param key: Settings key.
        :param default: Default value.
        :return: Settings value. Default value if key is not found.
        """
        return getattr(s, key, getattr(s, key.lower(), getattr(s, key.upper(), default)))

    def _add_celery_providers(self):
        self.providers['health'] += (
            ('celery', 'health_check.providers.celery.health.celery', None, {'workers': self.celery_workers}),
        )
        self.providers['stats'] += (
            ('celery', 'health_check.providers.celery.stats.celery', None, {'workers': self.celery_workers}),
        )

    @reset
    def build_from_module(self, module=None):
        if isinstance(module, str):
            module = self.import_settings(module)

        # Project path defined in settings
        self.base_dir = self.get(module, 'base_dir')

        # Celery application
        self.celery_workers = self.get(module, 'health_check_celery_workers', ())

        # Mapping of resources to list of providers
        # Each provider is a tuple of application name, provider, args, kwargs
        self.providers = self.get(module, 'health_check_providers', {
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

    @reset
    def build_from_django(self):
        from django.conf import settings as django_settings

        # Django debug settings.
        self.debug = self.get(django_settings, 'DEBUG', False)

        # Django installed apps
        self.installed_apps = self.get(django_settings, 'INSTALLED_APPS', [])
        self.caches = self.get(django_settings, 'CACHES', {})

        # Project path defined in Django settings
        self.base_dir = self.get(django_settings, 'BASE_DIR')

        # Celery application
        self.celery_workers = self.get(django_settings, 'HEALTH_CHECK_CELERY_WORKERS', ())

        # Mapping of resources to list of providers
        # Each provider is a tuple of application name, provider, args, kwargs
        self.providers = self.get(django_settings, 'HEALTH_CHECK_PROVIDERS', {
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
