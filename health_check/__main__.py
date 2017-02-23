# -*- coding: utf-8 -*-
import sys

from health_check.commands import HealthCheckCommand

__all__ = ['main']


def main():
    return HealthCheckCommand().run()


if __name__ == '__main__':
    sys.exit(main())
