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
