#!/usr/local/env python
# -*- coding: utf-8 -*-
import argparse
import shlex
import sys

import nose
import prospector.run as prospector


class RunTests:
    description = 'Run lint and tests'

    def __init__(self):
        parsed_args = self.parse_arguments()
        self.test_module = parsed_args['test_module']
        self.test_args = shlex.split(' '.join(parsed_args['test_args']))
        self.skip_lint = parsed_args['skip_lint']
        self.skip_tests = parsed_args['skip_tests']
        self.exit_on_fail = parsed_args['exit_on_fail']

    def add_arguments(self, parser):
        parser.add_argument('--skip-lint', action='store_true', help='Skip lint')
        parser.add_argument('--skip-tests', action='store_true', help='Skip tests')
        parser.add_argument('-e', '--exit-on-fail', action='store_true', help='Exit on step fail')
        parser.add_argument('test_module', nargs='*', default=['.'], help='Module to test')
        parser.add_argument('--test_args', action='store', default=[], nargs=argparse.REMAINDER,
                            help='Extra arguments to pass to tests')

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description=self.description)
        self.add_arguments(parser)
        return {k: v for k, v in vars(parser.parse_args()).items()}

    def tests(self):
        argv = ['nosetests'] + self.test_module + self.test_args
        result = nose.run(argv=argv)
        return (result + 1) % 2  # Change 0 to 1 and 1 to 0

    def lint(self):
        argv = sys.argv
        sys.argv = []
        result = prospector.main()
        sys.argv = argv
        return result

    def _check_exit(self, result):
        print('Return code: {:d}'.format(result))
        if self.exit_on_fail and result:
            sys.exit(result)

    def run(self):
        if not self.skip_lint:
            self._check_exit(self.lint())

        if not self.skip_tests:
            self._check_exit(self.tests())


if __name__ == '__main__':
    sys.exit(RunTests().run())
