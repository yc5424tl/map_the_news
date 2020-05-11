from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    username = models.TextField(_('username'), max_length=254, unique=True)
    first_name = models.TextField(_('first name'), max_length=254, null=True, blank=True)
    middle_initial = models.TextField(_('middle initial'), max_length=1, null=True, blank=True)
    last_name = models.TextField(_('last name'), max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def get_absolute_url(self):
        return f'/users/{self.pk}/'

    @property
    def full_name(self):
        first = self.first_name if self.first_name is not None else ''
        middle = f'{self.middle_initial}. ' if self.middle_initial is not None and self.middle_initial != '' else ''
        last = self.last_name if self.last_name is not None else ''
        return f'{first} {middle}{last}'