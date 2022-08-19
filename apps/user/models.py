from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

from lib.models import BaseModel
from .managers import UserManager


def user_picture_bucket(instance, filename):
    return f'{instance.email}/pictures/{filename}'


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    name = models.CharField(_('full name'), max_length=100, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into '
                    'this admin site.'))
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be '
                    'treated as active. Unselect this instead of deleting '
                    'accounts.'))
    picture = models.ImageField(
        upload_to=user_picture_bucket,
        null=True,
        blank=True,
        verbose_name=_('profile picture')
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        """
        Returns the first name for the user.
        """
        return self.name.split(' ')[0]

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        from_email = from_email or settings.DEFAULT_FROM_EMAIL
        send_mail(subject, message, from_email, [self.email], **kwargs)
