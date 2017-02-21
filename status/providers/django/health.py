# -*- coding: utf-8 -*-
"""
Built-in Django check providers.
"""
import datetime

from django.core.cache import caches as django_caches
from django.db import connections

from status.settings import settings


def databases(*args, **kwargs):
    """
    Check database status.

    :return: Status of each database.
    """
    status = {}
    for connection in connections.all():
        try:
            connection.connect()
            status[connection.alias] = connection.is_usable()
        except:
            status[connection.alias] = False

    return status


def caches(*args, **kwargs):
    """
    Check caches status.

    :return: Status of each cache.
    """
    caches_aliases = settings.caches.keys()
    value = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    status = {}
    for alias in caches_aliases:
        try:
            cache = django_caches[alias]
            cache.set('django_status_test_cache', value)
            status[alias] = True
        except:
            status[alias] = False

    return status
