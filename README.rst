=============
Django Status
=============

:Version: 1.2.0
:Status: Production/Stable
:Author: José Antonio Perdiguero López

Django Status is a application for Django projects that provides an API to check the status of some parts and some
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
    URL: /api/ping

Code
    Source code stats such as current active branch, last commit, if debug is active...
    URL: /api/code

Databases
    Check if databases are running.
    URL: /api/databases

Databases stats
    Show stats for all databases.
    URL: /api/databases/stats

Caches
    Check if caches are running.
    URL: /api/caches

Celery
    Check if celery workers defined in settings are running.
    URL: /api/celery

Celery stats
    Show celery worker stats.
    URL: /api/celery/stats

Settings
========
STATUS_CHECK_PROVIDERS
----------------------
List of additional check providers. Each provider consists in a tuple of name, function complete path, args and kwargs.
Example::

    STATUS_CHECK_PROVIDERS = (
        ('test', 'application.module.test_function', [1, 2], {'foo': 'bar'}),
    )

Default::

    STATUS_CHECK_PROVIDERS = (
        ('ping', 'status.check_providers.ping', None, None),
        ('code', 'status.check_providers.code', None, None),
        ('databases', 'status.check_providers.databases', None, None),
        ('databases/stats', 'status.check_providers.databases_stats', None, None),
        ('caches', 'status.check_providers.caches', None, None),
    )

STATUS_CELERY_WORKERS
---------------------
List of hostname from celery workers to be checked.
Default::

    STATUS_CELERY_WORKERS = ()

