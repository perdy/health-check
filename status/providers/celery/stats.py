# -*- coding: utf-8 -*-
"""
Built-in Celery check providers.
"""

from status.utils import FakeChecker

try:
    from celery.task import control

    celery_inspect = control.inspect()
except ImportError:
    celery_inspect = FakeChecker()


def celery(workers, *args, **kwargs):
    """
    Retrieve the stats data of given celery workers.

    :param workers: List of workers.
    :return: Stats data of each worker.
    """
    try:
        active_workers = celery_inspect.stats() or {}
        workers_stats = {k: v for k, v in active_workers.items() if k in workers}
    except AttributeError:
        workers_stats = None

    return workers_stats
