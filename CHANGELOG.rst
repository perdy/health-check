Changes
=======
v2.0.0 - 2/09/2016
 * Raise exception if incorrect provider given in settings.
 * Group providers by resource, adding two by default. *Health* resource manages health checks and *Stats* resource
reports a detailed status.

v1.3.0 - 31/08/2016
 * Separate api from main application.

v1.2.1 - 31/08/2016
 * Added compatibility with Django 1.10

v1.2.0 - 17/05/2016
 * Add root view for status api.
 * Use BASE_DIR instead of PROJECT_PATH to discover source code repo.+
 * Change default checks to be able to override.

v1.1.2 - 8/04/2016
 * Add source code stats.

v1.0.5 - 20/01/2016
 * Fix setup.py problems with requirements file.

v1.0.4 - 14/12/2015
 * Fix setup.py problems with utf-8 files.

v1.0.3 - 14/10/2015
 * Fix checkers for celery and celery stats. Now displays if a worker isn't running.

v1.0.2 - 14/10/2015
 * Update README and meta info.

v1.0.0 - 14/10/2015
 * Database check.
 * Database stats.
 * Cache check.
 * Celery check.
 * Celery stats.
 * First stable version.

v0.1.0 - 8/10/2015
 * Initial release.
