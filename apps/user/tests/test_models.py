import pytest
from model_bakery import baker

from django.core import mail

from apps.user.models import user_picture_bucket
from lib.test.generics import GenericTestModel


class TestUser(GenericTestModel):
    """Test User model"""

    def create_instance(self, *args, **kwargs):
        return baker.make('user.User', *args, **kwargs)

    @pytest.mark.django_db
    def test_picture_bucket(self):
        instances = self.create_instance(_quantity=2)
        assert (user_picture_bucket(instances[0], 'filename.png')
                != user_picture_bucket(instances[1], 'filename.png'))

    @pytest.mark.django_db
    def test_full_name(self):
        instance = self.create_instance(name='Gaius Julius Caesar')
        assert instance.get_full_name() == 'Gaius Julius Caesar'

    @pytest.mark.django_db
    def test_short_name(self):
        instance = self.create_instance(name='Gaius Julius Caesar')
        assert instance.get_short_name() == 'Gaius'

    @pytest.mark.django_db
    def test_email_user(self):
        instance = self.create_instance()
        instance.email_user('Título', 'Mensagem', 'pytest@tests.org')
        assert len(mail.outbox) == 1
        assert mail.outbox[0].body == 'Mensagem'
