# -*- coding: utf-8 -*-
from clinner.run import DjangoCommand
from health_check.commands import HealthCheckMain


class Command(DjangoCommand):
    """
    Wrapper that makes a Django command from TaskDispatcherCommand.
    """
    main_class = HealthCheckMain
