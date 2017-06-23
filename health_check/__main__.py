# -*- coding: utf-8 -*-
import sys

from health_check.commands import HealthCheckMain

__all__ = ['main']


def main():
    return HealthCheckMain().run()


if __name__ == '__main__':
    sys.exit(main())
