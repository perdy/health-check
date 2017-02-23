# -*- coding: utf-8 -*-
"""
URLs.
"""
from django.conf.urls import include, url
from django.views.generic import TemplateView

app_name = 'health_check'
urlpatterns = [
    url(r'^api/', include('health_check.api.urls')),
    url(r'^$', TemplateView.as_view(template_name='health_check/main.html')),
    url(r'^stats/?$', TemplateView.as_view(template_name='health_check/stats.html')),
    url(r'^health/?$', TemplateView.as_view(template_name='health_check/health.html')),
]
