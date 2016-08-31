# -*- coding: utf-8 -*-
"""
URLs.
"""
from django.conf.urls import include, url

urlpatterns = [
    url(r'^api/', include('status.api.urls')),
]
