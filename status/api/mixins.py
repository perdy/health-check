# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse


class ProviderMixin:
    def get_provider_url(self, request, resource, name):
        """
        Get provider url given resource and provider name.

        :param request: Django Request
        :param resource:
        :param name:
        :return:
        """
        return request.build_absolute_uri(reverse('status:api_{}_{}'.format(resource, name)))
