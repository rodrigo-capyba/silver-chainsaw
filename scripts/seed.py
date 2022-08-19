from safedelete import HARD_DELETE

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site


def run():
    print('running seed...')

    clear_data()

    # Change site domain and name.
    # Remember to change it via admin in each one of your application environments.
    site = Site.objects.get_current()
    site.domain = 'localhost:8000'
    site.name = 'Django Base'
    site.save()

    # user
    user = get_user_model().objects.create_user(
        email='user@capyba.com',
        password='test@123',
        name='Usuário de Teste',
    )
    admin = get_user_model().objects.create_superuser(
        email='admin@capyba.com',
        password='admin@123',
        name='Admin'
    )

    print('seed completed.')


def clear_data():
    # user
    get_user_model().objects.all().delete()


def _hard_delete(model):
    model.objects.all_with_deleted().delete(HARD_DELETE)