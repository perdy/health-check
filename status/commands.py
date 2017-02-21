# -*- coding: utf-8 -*-
import json
import sys
from argparse import ArgumentParser
from typing import Dict, Any

import yaml

from status.providers import Resource
from status.settings import settings


class StatusCommand:
    """
    Show status to console.
    """
    STATUS_HEALTH = 'health'
    STATUS_STATS = 'stats'
    STATUS_CHOICES = (STATUS_HEALTH, STATUS_STATS)

    OUTPUT_FORMAT_JSON = 'json'
    OUTPUT_FORMAT_YAML = 'yaml'
    OUTPUT_FORMAT_CHOICES = (OUTPUT_FORMAT_JSON, OUTPUT_FORMAT_YAML)

    description = 'Status command that provides a common entry point for running different checks providers'

    def __init__(self, parse_args=True, stdout=sys.stdout, stderr=sys.stderr):
        """
        Command for running producer, consumer and scheduler processes along with some other utilities.

        :param parse_args: If true, parse sys args.
        :param stdout: Standard output.
        :param stderr: Standard error.
        """
        self.args = self.parse_arguments() if parse_args else {}
        self.stdout = stdout
        self.stderr = stderr

    def add_arguments(self, parser: ArgumentParser, parser_class=None):
        subparsers_kwargs = {}
        if parser_class:
            subparsers_kwargs['parser_class'] = lambda **kwargs: parser_class(self, **kwargs)
        else:
            parser.add_argument('-s', '--settings', help='Settings module')

        subparsers = parser.add_subparsers(title='check', description='Status checks',
                                           dest='check', **subparsers_kwargs)
        subparsers.required = True

        # Health check
        parser_health = subparsers.add_parser(self.STATUS_HEALTH, help='Health checks')
        parser_health.add_argument(
            '-f', '--output_format', type=str, choices=self.OUTPUT_FORMAT_CHOICES, default=self.OUTPUT_FORMAT_YAML,
            help='Output format'
        )
        parser_health.add_argument(
            '-e', '--error_on_fail', action='store_true', default=False, help='Output format'
        )
        parser_health.set_defaults(func=self.health)

        # Stats
        parser_stats = subparsers.add_parser(self.STATUS_STATS, help='Components stats')
        parser_stats.add_argument(
            '-f', '--output_format', type=str, choices=self.OUTPUT_FORMAT_CHOICES, default=self.OUTPUT_FORMAT_YAML,
            help='Output format'
        )
        parser_stats.set_defaults(func=self.stats)

    def parse_arguments(self) -> Dict[str, Any]:
        """
        Parse sys args and transform it into a dict.

        :return: Arguments parsed in dict form.
        """
        parser = ArgumentParser(description=self.description)
        self.add_arguments(parser)
        return {k: v for k, v in vars(parser.parse_args()).items()}

    def health(self, output_format, *args, **kwargs):
        resource = Resource(kwargs['check'])

        data = resource()

        if output_format == self.OUTPUT_FORMAT_JSON:
            output = json.dumps(data)
        else:
            output = yaml.safe_dump(data, default_flow_style=False)

        self.stdout.write(output)

        if kwargs['error_on_fail'] and not all([value for provider in data.values() for value in provider.values()]):
            sys.exit(1)

    def stats(self, output_format, *args, **kwargs):
        resource = Resource(kwargs['check'])

        if output_format == self.OUTPUT_FORMAT_JSON:
            output = json.dumps(resource())
        else:
            output = yaml.safe_dump(resource(), default_flow_style=False)

        self.stdout.write(output)

    def run(self, **kwargs):
        """
        Command entrypoint.
        """
        kwargs = kwargs or self.args

        if not kwargs:
            raise ValueError('Arguments must be passed or parsed previously')

        if kwargs['settings']:
            settings.build_from_module(module=kwargs['settings'])

        command = kwargs['func']
        return command(**kwargs)
