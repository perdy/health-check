# -*- coding: utf-8 -*-
import json
import os
import sys

import logging
import warnings

import yaml
from clinner.command import command
from clinner.exceptions import ImproperlyConfigured
from clinner.run import Main

from health_check.settings import settings
from health_check.providers import Resource

OUTPUT_FORMAT_JSON = 'json'
OUTPUT_FORMAT_YAML = 'yaml'
OUTPUT_FORMAT_CHOICES = (OUTPUT_FORMAT_JSON, OUTPUT_FORMAT_YAML)

logger = logging.getLogger('cli')


def _print_resource(data, output_format):
    """
    Prints resource info using given format.
    
    :param data: Resource info.
    :param output_format: Output format.
    """
    if output_format == OUTPUT_FORMAT_JSON:
        output = json.dumps(data)
    else:
        output = yaml.safe_dump(data, default_flow_style=False)

    logger.info(output)


@command(args=((('-e', '--error-on-fail'), {'help': 'Returns error code if a health provider fails',
                                            'action': 'store_true', 'default': False}),
               (('-f', '--output-format'), {
                   'help': 'Output format', 'choices': OUTPUT_FORMAT_CHOICES,
                   'default': OUTPUT_FORMAT_YAML
               }),
               (('provider',), {'help': 'Providers to be used for checking', 'nargs': '*'})),
         parser_opts={'help': 'Run health providers'})
def health(*args, **kwargs):
    warnings.warn('This command is deprecated. Use "check health" command instead.', DeprecationWarning)

    data = Resource('health')(kwargs.get('provider'))

    _print_resource(data, kwargs['output_format'])

    if kwargs['error_on_fail'] and not all([value for provider in data.values() for value in provider.values()]):
        sys.exit(1)


@command(args=((('-f', '--output-format'), {'help': 'Output format', 'choices': OUTPUT_FORMAT_CHOICES,
                                            'default': OUTPUT_FORMAT_YAML}),
               (('provider',), {'help': 'Providers to be used for checking', 'nargs': '*'})),
         parser_opts={'help': 'Run stats providers'})
def stats(*args, **kwargs):
    warnings.warn('This command is deprecated. Use "check stats" command instead.', DeprecationWarning)

    data = Resource('stats')(kwargs.get('provider'))

    _print_resource(data, kwargs['output_format'])


@command(args=((('-e', '--error-on-fail'), {'help': 'Returns error code if a health provider fails',
                                            'action': 'store_true', 'default': False}),
               (('-f', '--output-format'), {
                   'help': 'Output format', 'choices': OUTPUT_FORMAT_CHOICES,
                   'default': OUTPUT_FORMAT_YAML
               }),
               (('resource',), {'help': 'Resource to check'}),
               (('provider',), {'help': 'Providers to be used for checking', 'nargs': '*'})),
         parser_opts={'help': 'Run health providers'})
def check(*args, **kwargs):
    data = Resource(kwargs.get('resource'))(kwargs.get('provider'))

    _print_resource(data, kwargs['output_format'])

    if kwargs['error_on_fail'] and not all([value for provider in data.values() for value in provider.values()]):
        sys.exit(1)


class HealthCheckMain(Main):
    """
    Command for running producer, consumer and scheduler processes along with some other utilities. This acts as a
    Command Line Interface for Task dispatcher.
    """
    description = 'Health check command that provides a common entry point for running the different checks'

    def inject_app_settings(self):
        if self.settings:
            os.environ['HEALTH_CHECK_SETTINGS'] = self.settings

        if 'HEALTH_CHECK_SETTINGS' not in os.environ:
            raise ImproperlyConfigured('Settings not defined')

        settings.build_from_module(os.environ['HEALTH_CHECK_SETTINGS'])
