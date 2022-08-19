import pytest
from model_bakery import baker

from django.contrib.auth import get_user_model


@pytest.fixture
def user():
    return get_user_model().objects.create_user('user@test.com', '123456')


@pytest.fixture
def admin_user():
    return get_user_model().objects.create_superuser('admin@test.com', '123456')


@pytest.fixture
def admin_client(db, admin_user):
    """A Django test client logged in as an admin user."""
    from django.test.client import Client

    client = Client()
    client.user = admin_user
    client.force_login(admin_user)
    return client


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def api_client_with_credentials(db, api_client, user):
    api_client.user = user
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)
