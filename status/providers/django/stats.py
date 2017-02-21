# -*- coding: utf-8 -*-
"""
Built-in Django check providers.
"""

from django.db import connections


def databases(*args, **kwargs):
    """
    Retrieve the stats data of each database.

    :return: Stats data of each database.
    """
    stats = {}
    for connection in connections.all():
        try:
            connection.connect()
        except:
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
