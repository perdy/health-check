=============
Django Status
=============

:Version: 2.0.0
:Status: Production/Stable
:Author: José Antonio Perdiguero López

Django Status is an application for Django projects that provides an API to check the status of some parts and some
utilities like ping requests.

Quick start
===========

#. Install this package using pip::

    pip install django-status


#. Add *PROJECT_PATH* to your django settings module.
#. Add *status* to your **INSTALLED_APPS** settings like this::

    INSTALLED_APPS = (
        ...
        'status',
    )

#. Add **Django-status** urls to your project urls::

    urlpatterns = [
        ...
        url(r'^status/', include('status.urls')),
    ]

Django Status API
=================
Django Status API can be used as a standalone application including only their urls::

    urlpatterns = [
        ...
        url(r'^status/', include('status.api.urls')),
    ]

This API have a single url for each provider, that are grouped by resources.
Each provider can be queried alone, returning his current status::

    http://your_domain/status/api/health/ping

Also there is a resource view that will return the status of all providers::

    http://your_domain/status/api/health

For last, there is a root view that will return the status of all providers from all resources::

    http://your_domain/status/api

Check Providers
===============
Django Status provides a mechanism to add new custom check functions through **check providers**. Each check provider
will generate a new API method with an URL that uses the name of the provider. These functions must accept \*args and
\*\*kwargs and will return a JSON-serializable object through json.dumps() method, for example a ping function::

    def ping(*args, **kwargs):
        return {'pong': True}

By default **Django status** provides the follow checks:

Ping
    A ping to application.
    URL: /api/health/ping

Databases
    Check if databases are running.
    URL: /api/health/databases

Caches
    Check if caches are running.
    URL: /api/health/caches

Celery
    Check if celery workers defined in settings are running.
    URL: /api/health/celery

Databases stats
    Show stats for all databases.
    URL: /api/stats/databases

Celery stats
    Show celery worker stats.
    URL: /api/stats/celery

Code
    Source code stats such as current active branch, last commit, if debug is active...
    URL: /api/stats/code

Settings
========
STATUS_CHECK_PROVIDERS
----------------------
List of additional check providers. Each provider consists in a tuple of name, function complete path, args and kwargs.
Example::

    STATUS_PROVIDERS = {
        'resource': (
            ('test', 'application.module.test_function', [1, 2], {'foo': 'bar'}),
        )
    }

Default::

    PROVIDERS = getattr(settings, 'STATUS_PROVIDERS', {
        'health': (
            ('ping', 'status.providers.health.ping', None, None),
            ('databases', 'status.providers.health.databases', None, None),
            ('caches', 'status.providers.health.caches', None, None),
        ),
        'stats': (
            ('databases', 'status.providers.stats.databases', None, None),
            ('code', 'status.providers.stats.code', None, None),
        )
    }

STATUS_CELERY_WORKERS
---------------------
List of hostname from celery workers to be checked. If any worker is defined, two additional providers listed previously
will be added to default set.
Default::

    STATUS_CELERY_WORKERS = ()

