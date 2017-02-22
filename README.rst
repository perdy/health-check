=============
Django Status
=============

:Version: 2.2.1
:Status: Production/Stable
:Author: José Antonio Perdiguero López

Django Status is an application that provides an API to check the status of some parts and some utilities like ping
requests. This application can works as standalone or included in a Django project.

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

Django Status website
=====================
A website that shows Django Status data is available in this application. It's possible access to follow URLs to get a
detailed view of your system status. Those three pages will show results of providers configured (as explained in
settings section)::

    http://www.website.com/status/
    http://www.website.com/status/health/
    http://www.website.com/status/stats/

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

Django management commands
==========================
Django Status provides a django management command to query current status of a resource. This command can be call as::

    python manage.py status <resource> [options]

To get current status of health checks, and exit with an error if some check is failing::

    python manage.py status health -e

Each resource has its own set of options that can be displayed through command help::

    python manage.py status -h

Command
=======
Previous Django command can be used in standalone mode as::

    django_status <resource> [options]

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
            ('databases', 'status.providers.django.health.databases', None, None),
            ('caches', 'status.providers.django.health.caches', None, None),
        ),
        'stats': (
            ('databases', 'status.providers.django.stats.databases', None, None),
            ('code', 'status.providers.stats.code', None, None),
        )
    }

STATUS_CELERY_WORKERS
---------------------
List of hostname from celery workers to be checked. If any worker is defined, two additional providers listed previously
will be added to default set.
Default::

    STATUS_CELERY_WORKERS = ()

