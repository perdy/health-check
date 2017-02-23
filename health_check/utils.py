# -*- coding: utf-8 -*-
"""
Utils.
"""


class FakeChecker(object):
    def __getattribute__(self, item):
        return lambda *args, **kwargs: None
