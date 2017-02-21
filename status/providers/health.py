# -*- coding: utf-8 -*-
"""
Built-in check providers.
"""


def ping(*args, **kwargs):
    """
    Check if current application is running.

    :return: Pong response.
    """

    return {'pong': True}
