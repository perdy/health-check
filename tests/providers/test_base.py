import pytest
from unittest.mock import patch

from health_check.providers import Provider, Resource
from health_check.settings import settings


def foo_provider(*args, **kwargs):
    return {
        'foo': True
    }


def bar_provider(*args, **kwargs):
    return {
        'bar': False
    }


class TestResource:
    @pytest.fixture()
    def providers(self):
        return {
            'foobar': (
                ('foo', 'tests.providers.test_base.foo_provider', None, None),
                ('bar', 'tests.providers.test_base.bar_provider', None, None),
            )
        }

    @pytest.fixture()
    def settings_mock(self):
        with patch('health_check.providers.base.settings') as s:
            yield s

    @pytest.mark.high
    @pytest.mark.provider
    def test_provider(self):
        expected_result = {'foo': True}
        provider = Provider('foo', foo_provider, None, None)

        result = provider()

        assert result == expected_result

    @pytest.mark.high
    @pytest.mark.provider
    def test_provider_dynamic_import(self):
        expected_result = {'foo': True}
        provider = Provider('foo', 'tests.providers.test_base.foo_provider', None, None)

        result = provider()

        assert result == expected_result

    @pytest.mark.low
    @pytest.mark.provider
    def test_provider_wrong(self):
        with pytest.raises(ValueError):
            Provider('foo', 'tests.providers.test_base.wrong_provider', None, None)

    @pytest.mark.high
    @pytest.mark.provider
    def test_resource(self, providers, settings_mock):
        expected_result = {
            'foo': {'foo': True},
            'bar': {'bar': False},
        }
        settings_mock.providers = providers
        resource = Resource('foobar')

        result = resource()

        assert result == expected_result

    @pytest.mark.high
    @pytest.mark.provider
    def test_resource_filter_providers(self, providers, settings_mock):
        expected_result = {
            'bar': {'bar': False},
        }
        settings_mock.providers = providers
        resource = Resource('foobar')

        result = resource(['bar'])

        assert result == expected_result

    @pytest.mark.low
    @pytest.mark.provider
    def test_resource_wrong(self):
        with pytest.raises(ValueError):
            Resource('foo')
