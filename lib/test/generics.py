import pytest

from django.apps import apps
from django.conf import settings
from django.urls import reverse

from . import mixins


class GenericTestModel:
    """Generic class to test models."""

    def create_instance(self, *args, **kwargs):
        raise NotImplementedError('Subclasses should implement this method!')

    @pytest.mark.django_db
    def test_str(self):
        instance = self.create_instance()
        str(instance)
        assert True


class GenericTestSerializer:
    """Generic class to test serializers."""
    # You'll need to set this attribute.
    serializer_class = None

    def get_data(self):
        return {}

    def get_serializer(self, *args, **kwargs):
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer()` method."
            % self.__class__.__name__
        )
        return self.serializer_class(*args, **kwargs)

    @pytest.mark.django_db
    def test_is_valid(self):
        data = self.get_data()
        serializer = self.get_serializer(data=data)
        assert serializer.is_valid(), serializer.errors


class GenericTestAPIView:
    """Generic class to test APIView.

    Includes:
    - authorization test (login required by default)
    """
    # You'll need to either set these attributes, or override `get_url()`.
    url_basename = None
    default_action = None

    # If you want to test for permissions.
    allowed_user_types = None

    def get_url(self, action=None, *args):
        """
        Get a url by name, using django's reverse function.
        Uses `url_basename` and a given action to assemble the url name.
        If action is not passed, `default_action` is used, if it is defined.
        Other arguments received by this function are passed to reverse().
        """
        assert self.url_basename is not None, (
            "'%s' should either include a `url_basename` attribute, "
            "or override the `get_url()` method."
            % self.__class__.__name__
        )
        if action:
            suffix = f'-{action}'
        else:
            suffix = f'-{self.default_action}' if self.default_action else ''
        return reverse(self.url_basename + suffix, args=args)

    def get_forbidden_types(self):
        """
        Return a list of forbidden user types to this view,
        based on `allowed_user_types`.

        [forbidden types] = [all user types] - [allowed_user_types]
        """
        allowed_user_types = self.allowed_user_types or []
        types = apps.get_model(settings.AUTH_USER_MODEL).TYPE_CHOICES
        return [t[0] for t in types if t[0] not in allowed_user_types]


class AuthenticatedViewTest(mixins.IsAuthenticatedMixin,
                            GenericTestAPIView):
    """
    Concrete view that requires authentication.
    """
    pass
