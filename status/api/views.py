# -*- coding: utf-8 -*-
"""
Views for status API.
"""
from django.http import JsonResponse
from django.views.generic import View
from django.views.generic.base import ContextMixin

from status.settings import settings
from status.api.mixins import ProviderMixin
from status.providers.base import Provider, Resource

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


class RootAPIView(ProviderMixin, APIView):
    """
    Root API view that routes to each single ProviderAPIView
    """

    def __init__(self):
        super(RootAPIView, self).__init__()
        self.resources = {resource: Resource(resource) for resource in settings.providers}

    def get(self, request, *args, **kwargs):
        """
        Create an object that contains all resources and within them, all providers with their current status.

        Mapping of resource to another mapping of provider to status.
        Resource -> {Provider -> Status}

        :param request: Request.
        :return: Rendered response.
        """
        context = {resource.name: resource() for resource in self.resources.values()}
        return self.render_to_response(context)

    def options(self, request, *args, **kwargs):
        """
        List all providers of current resource with their absolute urls for each resource

        Mapping of resource to another mapping of provider to url.
        Resource -> {Provider -> URL}

        :param request: Request.
        :return: Rendered response.
        """
        context = {resource.name: {provider_name: self.get_provider_url(request, resource.name, provider_name)
                                   for provider_name in resource.providers.keys()}
                   for resource in self.resources.values()}
        return self.render_to_response(context)


class ResourceAPIView(ProviderMixin, APIView):
    """
    Root API view for a resource. List all checks
    """
    resource = None

    def __init__(self, resource, **kwargs):
        super(ResourceAPIView, self).__init__()
        self.resource = Resource(resource)

    def get_context_data(self, **kwargs):
        return self.resource()

    def options(self, request, *args, **kwargs):
        """
        List all providers of current resource with their absolute urls.

        Mapping of provider to url.
        Provider -> URL

        :param request: Request.
        :return: Rendered response.
        """
        context = {name: self.get_provider_url(request, self.resource.name, name)
                   for name in self.resource.providers.keys()}
        return self.render_to_response(context)


class ProviderAPIView(APIView):
    """
    Specific class that uses a given provider.
    """
    provider = None
    provider_name = None
    provider_args = None
    provider_kwargs = None

    def __init__(self, provider_name, provider, provider_args, provider_kwargs, **kwargs):
        self.provider = Provider(provider_name, provider, provider_args, provider_kwargs)
        super(ProviderAPIView, self).__init__(**kwargs)

    def get_context_data(self):
        return self.provider()
