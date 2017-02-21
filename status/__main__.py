# -*- coding: utf-8 -*-
import sys

from status.commands import StatusCommand

__all__ = ['main']


def main():
    return StatusCommand().run()


if __name__ == '__main__':
    sys.exit(main())
