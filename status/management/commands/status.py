# -*- coding: utf-8 -*-
import json
import sys

import yaml
from django.core.management import BaseCommand, CommandParser
from django.utils.translation import ugettext_lazy as _
from status.providers import Resource


class Command(BaseCommand):
    """
    Show status to console.
    """
    STATUS_HEALTH = 'health'
    STATUS_STATS = 'stats'
    STATUS_CHOICES = ()

    OUTPUT_FORMAT_JSON = 'json'
    OUTPUT_FORMAT_YAML = 'yaml'
    OUTPUT_FORMAT_CHOICES = (OUTPUT_FORMAT_JSON, OUTPUT_FORMAT_YAML)

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(
            title='status', description='Status checks', dest='status',
            parser_class=lambda **kwargs: CommandParser(self, **kwargs)
        )

        # Health check
        parser_health = subparsers.add_parser(self.STATUS_HEALTH, help=_('Health checks'))
        parser_health.add_argument(
            '-f', '--output_format', type=str, choices=self.OUTPUT_FORMAT_CHOICES, default=self.OUTPUT_FORMAT_YAML,
            help='Output format'
        )
        parser_health.add_argument(
            '-e', '--error_on_fail', action='store_true', default=False, help='Output format'
        )

        # Stats
        parser_stats = subparsers.add_parser(self.STATUS_STATS, help=_('Components stats'))
        parser_stats.add_argument(
            '-f', '--output_format', type=str, choices=self.OUTPUT_FORMAT_CHOICES, default=self.OUTPUT_FORMAT_YAML,
            help='Output format'
        )

    def handle_health(self, output_format, *args, **kwargs):
        resource = Resource(kwargs['status'])

        data = resource()

        if output_format == self.OUTPUT_FORMAT_JSON:
            output = json.dumps(data)
        else:
            output = yaml.dump(data, default_flow_style=False)

        self.stdout.write(output)

        if kwargs['error_on_fail'] and not all([value for provider in data.values() for value in provider.values()]):
            sys.exit(1)

    def handle_stats(self, output_format, *args, **kwargs):
        resource = Resource(kwargs['status'])

        if output_format == self.OUTPUT_FORMAT_JSON:
            output = json.dumps(resource())
        else:
            output = yaml.dump(resource(), default_flow_style=False)

        self.stdout.write(output)

    def handle(self, *args, **options):
        status = options['status']

        if status == self.STATUS_HEALTH:
            self.handle_health(*args, **options)
        elif status == self.STATUS_STATS:
            self.handle_stats(*args, **options)
