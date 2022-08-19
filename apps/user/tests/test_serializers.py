import pytest

from apps.user.serializers import UserSerializer


class TestUserSerializer:
    """Test UserSerializer"""

    @pytest.fixture
    def serializer_class(self):
        return UserSerializer

    @pytest.fixture
    def serializer_data(self):
        return {
            'email': 'user@test.com',
            'username': 'testuser',
        }

    @pytest.mark.django_db
    def test_is_valid(self, serializer_class, serializer_data):
        serializer = serializer_class(data=serializer_data)
        assert serializer.is_valid(), serializer.errors
