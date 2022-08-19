import pytest
from model_bakery import baker
from rest_framework import status


class IsAuthenticatedMixin:
    """
    Require authentication to acess resource.
    """
    @pytest.mark.django_db
    def test_authorization(self, api_client):
        response = api_client.get(self.get_url())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.status_code


class UserTypePermissionMixin:
    """
    Only users form a certain type may access resource.
    """
    @pytest.mark.django_db
    def test_permissions(self, api_client):
        for type_ in self.get_forbidden_types():
            user = baker.make('user.User', type=type_)
            api_client.force_authenticate(user=user)
            response = api_client.get(self.get_url())
            assert response.status_code == status.HTTP_403_FORBIDDEN, response.status_code
            api_client.force_authenticate(user=None)
