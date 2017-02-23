# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os


PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
APP_PATH = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(os.path.join(PROJECT_PATH, '..'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'default-cache',
    },
    'demo': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'demo-cache',
    }
}

ALLOWED_HOSTS = ['*']

TIME_ZONE = 'Europe/Madrid'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = PROJECT_PATH + '/media/'

MEDIA_URL = '/media/'

STATIC_ROOT = PROJECT_PATH + '/static/'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(APP_PATH, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = '3+&amp;*6eq%(gs1heqnu!fpb%&amp;#16_^3x#s_nh04^7dxa8tgb%meu'

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

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'demo.urls'

WSGI_APPLICATION = 'demo.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(APP_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'demo',
    'health_check',
)

HEALTH_CHECK_CELERY_WORKERS = (
    'demo_worker',
)
