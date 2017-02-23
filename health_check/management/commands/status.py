# -*- coding: utf-8 -*-
try:
    from django.core.management.base import BaseCommand, CommandParser
except ImportError:
    BaseCommand = object

from health_check.commands import HealthCheckCommand


class Command(BaseCommand):
    """
    Wrapper that makes a Django command from TaskDispatcherCommand.
    """
    help = HealthCheckCommand.description

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.command = HealthCheckCommand(parse_args=False, stdout=self.stdout, stderr=self.stderr)

    def add_arguments(self, parser):
        self.command.add_arguments(parser=parser, parser_class=CommandParser)

    def handle(self, *args, **options):
        self.command.run(**options)
