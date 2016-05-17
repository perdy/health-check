# -*- coding: utf-8 -*-
"""
Built-in check providers.
"""
import datetime
from django.db import connections, OperationalError
from django.core.cache import caches as django_caches, InvalidCacheBackendError
from git import Repo
from git.exc import InvalidGitRepositoryError

from status.settings import CACHES, DEBUG, BASE_DIR

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


def celery_stats(workers, *args, **kwargs):
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
        except OperationalError:
            status[connection.alias] = False

    return status


def databases_stats(*args, **kwargs):
    """
    Retrieve the stats data of each database.

    :return: Stats data of each database.
    """
    stats = {}
    for connection in connections.all():
        try:
            connection.connect()
        except OperationalError:
            is_usable = False
        else:
            is_usable = connection.is_usable()
        finally:
            stats[connection.alias] = {
                'vendor': connection.vendor,
                'is_usable': is_usable,
                'allow_thread_sharing': connection.allow_thread_sharing,
                'autocommit': connection.autocommit,
                'commit_on_exit': connection.commit_on_exit,
                'in_atomic_block': connection.in_atomic_block,
                'settings': {k: v for k, v in connection.settings_dict.items() if k not in ('USER', 'PASSWORD')}
            }

    return stats


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
        except InvalidCacheBackendError:
            status[alias] = False

    return status


def code(*args, **kwargs):
    """
    Code stats, such as current branch, debug mode, last commit, etc.

    :return: Source code stats.
    """
    stats = {'debug': DEBUG}
    try:
        scm_stats = {'scm': 'git'}
        repo = Repo(BASE_DIR)

        # Branch info
        branch = repo.active_branch
        scm_stats['branch'] = {
            'local': branch.name,
        }
        try:
            # Try to get remote branch name
            scm_stats['branch']['remote'] = branch.tracking_branch().name,
        except:
            scm_stats['branch']['remote'] = 'unknown'

        # Last commit info
        commit = repo.commit(branch)
        scm_stats['commit'] = {
            'id': commit.hexsha,
            'summary': commit.summary,
            'author': commit.author.name,
            'date': datetime.datetime.fromtimestamp(commit.authored_date)
        }

        # Get tag info
        tag = None
        tags = repo.tags
        tags.reverse()
        for t in (t for t in tags if tag is None):
            if t.commit == commit:
                tag = t
        if tag:
            scm_stats['tag'] = tag.name
    except InvalidGitRepositoryError:
        scm_stats = {}

    stats.update(scm_stats)

    return stats
