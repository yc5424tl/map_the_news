from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager using email as unique identifier !username
    """
    def _create_user(self, email, password, username, first_name, last_name, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError(_('Email Required'))
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=True,
            first_name=first_name,
            last_name=last_name,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, username, first_name, last_name, **extra_fields):
        return self._create_user(email, password, username, first_name, last_name, False, False, **extra_fields)

    def create_superuser(self, email, password, username, first_name, last_name, **extra_fields):
        return self._create_user(email, password, username, first_name, last_name, True, True, **extra_fields)
