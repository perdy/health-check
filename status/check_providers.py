# -*- coding: utf-8 -*-
"""
Built-in check providers.
"""


def ping(*args, **kwargs):
    return {'ok': 'pong'}


def celery(*args, **kwargs):
    return {'ok': kwargs['app']}
