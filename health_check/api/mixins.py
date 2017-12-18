# -*- coding: utf-8 -*-
import django

if django.VERSION < (2, 0):
    from django.core.urlresolvers import reverse
else:
    from django.urls import reverse


class ProviderMixin:
    def get_provider_url(self, request, resource, name):
        """
        Get provider url given resource and provider name.

        :param request: Django Request
        :param resource:
        :param name:
        :return:
        """
        return request.build_absolute_uri(reverse('health_check:api_{}_{}'.format(resource, name)))
