# -*- coding: utf-8 -*-
"""
Built-in check providers.
"""
import datetime

from django.core.cache import caches as django_caches
from django.db import connections

from status.settings import CACHES
from status.utils import FakeChecker

try:
    from celery.task import control

    celery_inspect = control.inspect()
except ImportError:
    celery_inspect = FakeChecker()


def ping(*args, **kwargs):
    """
    Check if current application is running.

    :return: Pong response.
    """

    return {'pong': True}


def celery(workers, *args, **kwargs):
    """
    Check if given celery workers are running.

    :param workers: List of workers to be checked.
    :return: Status of each worker.
    """
    try:
        ping_response = celery_inspect.ping() or {}
        active_workers = ping_response.keys()
        workers_status = {w: w in active_workers for w in workers}
    except (AttributeError, OSError):
        workers_status = None

    return workers_status


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
    caches_aliases = CACHES.keys()
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
