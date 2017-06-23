Changes
=======
v3.1.1 - 2017/06/23
 * Minor bug fixing.

v3.1.0 - 2017/06/23
 * Improved and more flexible django command.

v3.0.0 - 2017/02/23
 * Move project from django-status to health-check.
 * Fix some bugs related to react item keys.

v2.3.0 - 2017/02/22
 * Specify settings through environment variable.
 * Change settings to lowercase.

v2.2.1 - 2017/02/21
 * Remove Django from requirements.

v2.2.0 - 2017/02/21
 * Add a standalone mode.
 * Command can be called as a Django command through manage.py or as a standlone script.

v2.1.0 - 2016/09/29
 * Create helpers to handle resources and providers and API refactor to use these helpers.
 * Create django management command that provides current status of a resource.

v2.0.0 - 2016/09/2
 * Raise exception if incorrect provider given in settings.
 * Group providers by resource, adding two by default. *Health* resource manages health checks and *Stats* resource
reports a detailed status.
 * Adds HTML views to display status of resources and providers.

v1.3.0 - 2016/08/31
 * Separate api from main application.

v1.2.1 - 2016/08/31
 * Added compatibility with Django 1.10

v1.2.0 - 2016/05/17
 * Add root view for status api.
 * Use BASE_DIR instead of PROJECT_PATH to discover source code repo.+
 * Change default checks to be able to override.

v1.1.2 - 2016/04/8
 * Add source code stats.

v1.0.5 - 2016/01/20
 * Fix setup.py problems with requirements file.

v1.0.4 - 2015/12/14
 * Fix setup.py problems with utf-8 files.

v1.0.3 - 2015/10/14
 * Fix checkers for celery and celery stats. Now displays if a worker isn't running.

v1.0.2 - 2015/10/14
 * Update README and meta info.

v1.0.0 - 2015/10/14
 * Database check.
 * Database stats.
 * Cache check.
 * Celery check.
 * Celery stats.
 * First stable version.

v0.1.0 - 2015/10/8
 * Initial release.
