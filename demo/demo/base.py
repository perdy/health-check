# -*- coding: utf-8 -*-
"""
Django settings.
"""

import os

from configurations import Configuration, values

__all__ = ['Base']


class DjangoRESTFrameworkMixin:
    """
    Django REST Framework configuration mixin.
    """
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
        'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
        'DEFAULT_FILTER_BACKENDS': (
            'rest_framework_filters.backends.DjangoFilterBackend',
        ),
    }

    REST_FRAMEWORK_DOCS = {
        'HIDE_DOCS': values.BooleanValue(False)
    }


class Base(DjangoRESTFrameworkMixin, Configuration):
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.SecretValue()

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False

    ALLOWED_HOSTS = ['']
    ADMINS = values.SingleNestedTupleValue((
        ('Jose Antonio Perdiguero', 'jose.perdiguero@piksel.com'),
        ('Miguel Barrientos', 'miguel.barrientos@piksel.com'),
        ('Ramon Acitores', 'ramon.acitores@piksel.com'),
        ('Michael Gordon', 'michael.gordon@piksel.com'),
        ('Gerald Chao', 'gerald.chao@piksel.com'),
    ))

    # Application definition

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # REST Framework
        'rest_framework',
        'rest_framework_docs',
        # Project apps
        'normuri',
        'core',
        # System utilities
        'gunicorn',
        'django_extensions',
        # Test
        'behave_django',
    )

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',
    )

    ROOT_URLCONF = 'normuri.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'normuri.wsgi.application'

    # Database
    DATABASES = {
        'default': {},
    }

    # Cache
    DEFAULT_CACHE_TIMEOUT = 60 * 15
    CACHES = {
        'default': {}
    }

    # Internationalization
    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'static'))
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        # other finders..
    )

    # Logging config
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'json': {
                '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
                'format': '%(asctime)s %(levelname)s %(name)s %(lineno)s %(message)s %(pathname)s %(module)s'
                          '%(funcName)s %(process)s'
            },
            'plain': {
                'format': '[%(asctime)s.%(msecs)dZ] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
                'datefmt': '%Y-%m-%dT%H:%M:%S',
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'plain'
            },
            'root_file': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': '/var/log/normuri/root.log',
                'formatter': 'plain',
                'when': 'midnight',
                'backupCount': 30,
                'utc': True
            },
            'base_file': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': '/var/log/normuri/base.log',
                'formatter': 'plain',
                'when': 'midnight',
                'backupCount': 30,
                'utc': True
            },
            'runserver_file': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': '/var/log/normuri/runserver.log',
                'formatter': 'plain',
                'when': 'midnight',
                'backupCount': 30,
                'utc': True
            },
            'request_file': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': '/var/log/normuri/request.log',
                'formatter': 'plain',
                'when': 'midnight',
                'backupCount': 30,
                'utc': True
            },
            'security_file': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': '/var/log/normuri/security.log',
                'formatter': 'plain',
                'when': 'midnight',
                'backupCount': 30,
                'utc': True
            },
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler',
                'include_html': True,
            },
        },
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            }
        },
        'loggers': {
            '': {
                'handlers': ['console', 'root_file', 'mail_admins'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'core': {
                'handlers': ['console', 'base_file', 'mail_admins'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'normuri': {
                'handlers': ['console', 'base_file', 'mail_admins'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'django.server': {
                'handlers': ['console', 'runserver_file'],
                'level': 'INFO',
                'propagate': True,
            },
            'django.request': {
                'handlers': ['console', 'request_file', 'mail_admins'],
                'level': 'INFO',
                'propagate': True,
            },
            'django.security': {
                'handlers': ['console', 'security_file', 'mail_admins'],
                'level': 'INFO',
                'propagate': True,
            },
        },
    }
