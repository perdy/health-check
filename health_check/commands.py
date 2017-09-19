# -*- coding: utf-8 -*-
import json
import os
import sys

import yaml
from clinner.command import command
from clinner.exceptions import ImproperlyConfigured
from clinner.run import Main

from health_check.settings import settings
from health_check.providers import Resource

OUTPUT_FORMAT_JSON = 'json'
OUTPUT_FORMAT_YAML = 'yaml'
OUTPUT_FORMAT_CHOICES = (OUTPUT_FORMAT_JSON, OUTPUT_FORMAT_YAML)


def _get_resource_filtered(resource_name, providers):
    """
    Get a resource by name and filter providers result with given list.
    
    :param resource_name: Resource name.
    :param providers: Providers list.
    :return: All providers info of given result.
    """
    resource = Resource(resource_name)

    data = resource()

    if providers and data:
        data = {k: v for k, v in data.items() if k in providers}

    return data


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

    print(output)


@command(args=((('-e', '--error-on-fail'), {'help': 'Returns error code if a health provider fails',
                                            'action': 'store_true', 'default': False}),
               (('-f', '--output-format'), {
                   'help': 'Output format', 'choices': OUTPUT_FORMAT_CHOICES,
                   'default': OUTPUT_FORMAT_YAML
               }),
               (('provider',), {'help': 'Providers to be used for checking', 'nargs': '*'})),
         parser_opts={'help': 'Run health providers'})
def health(*args, **kwargs):
    data = _get_resource_filtered('health', kwargs.get('provider'))

    _print_resource(data, kwargs['output_format'])

    if kwargs['error_on_fail'] and not all([value for provider in data.values() for value in provider.values()]):
        sys.exit(1)


@command(args=((('-f', '--output-format'), {'help': 'Output format', 'choices': OUTPUT_FORMAT_CHOICES,
                                            'default': OUTPUT_FORMAT_YAML}),
               (('provider',), {'help': 'Providers to be used for checking', 'nargs': '*'})),
         parser_opts={'help': 'Run stats providers'})
def stats(*args, **kwargs):
    data = _get_resource_filtered('stats', kwargs.get('provider'))

    _print_resource(data, kwargs['output_format'])


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
