# -*- coding: utf-8 -*-
"""
URLs.
"""
from django.conf.urls import include, url
from django.views.generic import TemplateView

app_name = 'status'
urlpatterns = [
    url(r'^api/', include('status.api.urls')),
    url(r'^$', TemplateView.as_view(template_name='status/main.html')),
    url(r'^stats/?$', TemplateView.as_view(template_name='status/stats.html')),
    url(r'^health/?$', TemplateView.as_view(template_name='status/health.html')),
]
