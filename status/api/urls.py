# -*- coding: utf-8 -*-
"""
URLs.
"""
from itertools import chain

from django.conf.urls import url

from status.settings import settings
from status.api.views import RootAPIView, ProviderAPIView, ResourceAPIView


def get_provider_urls(resource, providers):
    # Resource root view
    urls = [url(r'^{}/?$'.format(resource), ResourceAPIView.as_view(resource=resource),
                name='api_{}_root'.format(resource))]

    # Resource providers views
    urls += [url(r'^{}/{}/?$'.format(resource, n),
                 ProviderAPIView.as_view(provider=p, provider_name=n, provider_args=args, provider_kwargs=kwargs),
                 name='api_{}_{}'.format(resource, n))
             for n, p, args, kwargs in providers]

    return urls


providers_urls = chain.from_iterable([get_provider_urls(r, p) for r, p in settings.providers.items()])

urlpatterns = list(providers_urls)

urlpatterns += [
    url(r'^$', RootAPIView.as_view())
]
