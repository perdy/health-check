# -*- coding: utf-8 -*-
"""
URLs.
"""
from django.conf.urls import patterns, url

from status.views import ProviderAPIView, RootAPIView
from status import settings

urlpatterns = patterns('')

providers = [url(r'^api/{}/?$'.format(a),
                 ProviderAPIView.as_view(provider=p, provider_args=args, provider_kwargs=kwargs),
                 name='api_{}'.format(a))
             for a, p, args, kwargs in settings.CHECK_PROVIDERS]

urlpatterns += providers

urlpatterns += [url(r'^api/?$', RootAPIView.as_view())]
