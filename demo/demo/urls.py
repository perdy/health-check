# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # HealthCheck urls
    url(r'^health_check/', include('health_check.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
