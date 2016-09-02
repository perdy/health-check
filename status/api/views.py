# -*- coding: utf-8 -*-
"""
Views for status API.
"""
import importlib

from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.views.generic import View
from django.views.generic.base import ContextMixin

from status import settings

__all__ = ['ProviderAPIView', 'RootAPIView']


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """

    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        return context or {}


class JSONView(JSONResponseMixin, View):
    """
    View that returns a JSON response.
    """

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


class APIView(JSONView, ContextMixin):
    """
    Base class for API views.
    """

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class RootAPIView(APIView):
    """
    Root API view that routes to each single ProviderAPIView
    """

    def __init__(self):
        super(RootAPIView, self).__init__()
        self.providers = settings.PROVIDERS

    def _get_provider_url(self, request, resource, name):
        return request.build_absolute_uri(reverse('api_{}_{}'.format(resource, name)))

    def get(self, request, *args, **kwargs):
        """
        Create an object that contains all resources and within them, all providers with their current status.

        Mapping of resource to another mapping of provider to status.
        Resource -> {Provider -> Status}

        :param request: Request.
        :return: Rendered response.
        """
        context = {resource: {name: ProviderAPIView(provider, args, kwargs).get_context_data()
                              for name, provider, args, kwargs in providers}
                   for resource, providers in self.providers.items()}
        return self.render_to_response(context)

    def options(self, request, *args, **kwargs):
        """
        List all providers of current resource with their absolute urls for each resource

        Mapping of resource to another mapping of provider to url.
        Resource -> {Provider -> URL}

        :param request: Request.
        :return: Rendered response.
        """
        context = {resource: {name: self._get_provider_url(request, resource, name) for name, _, _, _ in providers}
                   for resource, providers in self.providers.items()}
        return self.render_to_response(context)


class ResourceAPIView(RootAPIView):
    """
    Root API view for a resource. List all checks
    """
    resource = None

    def __init__(self, resource, **kwargs):
        super(ResourceAPIView, self).__init__()
        self.resource = resource
        try:
            self.providers = settings.PROVIDERS[resource]
        except KeyError:
            raise ValueError("Resource doesn't exists: %s" % (resource,))

    def get(self, request, *args, **kwargs):
        """
        Create an object that contains all providers of current resource with their current status.

        Mapping of provider to status.
        Provider -> Status

        :param request: Request.
        :return: Rendered response.
        """
        context = {name: ProviderAPIView(provider=p, provider_args=args, provider_kwargs=kwargs).get_context_data()
                   for name, p, args, kwargs in self.providers}
        return self.render_to_response(context)

    def options(self, request, *args, **kwargs):
        """
        List all providers of current resource with their absolute urls.

        Mapping of provider to url.
        Provider -> URL

        :param request: Request.
        :return: Rendered response.
        """
        context = {name: self._get_provider_url(request, self.resource, name)
                   for name, _, _, _ in self.providers}
        return self.render_to_response(context)


class ProviderAPIView(APIView):
    """
    Specific class that uses a given provider.
    """
    provider = None
    provider_args = None
    provider_kwargs = None

    def __init__(self, provider, provider_args, provider_kwargs, **kwargs):
        if isinstance(provider, str):
            provider_module, provider_func = provider.rsplit('.', 1)
            module = importlib.import_module(provider_module)
            self.provider = getattr(module, provider_func, None)
            if self.provider is None:
                raise ValueError('Provider not found: %s' % (provider,))
        else:
            self.provider = provider

        self.provider_args = provider_args or ()
        self.provider_kwargs = provider_kwargs or {}

        super(ProviderAPIView, self).__init__(**kwargs)

    def get_context_data(self):
        return self.provider(*self.provider_args, **self.provider_kwargs)
