import json

import pytest
from model_bakery import baker

from django.urls import reverse

from rest_framework import status

from apps.user.models import User


class TestUserView:
    """Test UserView"""

    @pytest.mark.django_db
    def test_authorization(self, api_client):
        url = reverse('v1:user-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_list(self, api_client_with_credentials):
        baker.make('user.User', _quantity=2)

        url = reverse('v1:user-list')
        response = api_client_with_credentials.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['count'] == 3  # include authenticated user

    @pytest.mark.django_db
    def test_create(self, api_client_with_credentials):
        data = {
            'email': 'user2@test.com',
        }

        url = reverse('v1:user-list')
        response = api_client_with_credentials.post(
            url, data=json.dumps(data), content_type='application/json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email='user2@test.com').exists()

    @pytest.mark.django_db
    def test_detail(self, api_client_with_credentials):
        user = baker.make('user.User')

        url = reverse('v1:user-detail', args=[user.id])
        response = api_client_with_credentials.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['id'] == user.id

    @pytest.mark.django_db
    def test_update(self, api_client_with_credentials):
        user = baker.make('user.User', name='name1')
        data = {
            'name': 'name2',
        }

        url = reverse('v1:user-detail', args=[user.id])
        response = api_client_with_credentials.patch(
            url, data=json.dumps(data), content_type='application/json'
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['name'] == 'name2'

    @pytest.mark.django_db
    def test_delete(self, api_client_with_credentials):
        user = baker.make('user.User', email='to_be_deleted@test.com')

        url = reverse('v1:user-detail', args=[user.id])
        response = api_client_with_credentials.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(email='to_be_deleted@test.com').exists()
