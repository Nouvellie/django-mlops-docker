import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
from typing import (
    Dict,
    Generic,
    List,
    TypeVar,
)
NewUser = TypeVar('NewUser')


class UserManager(BaseUserManager):
    """Creates a modified class based on BaseUserManager."""

    def create_user(self, username: str, email: str, password: str, **other_fields) -> Generic[NewUser]:
        """User creation."""
        if not email:
            raise ValueError(_("You must provide an email address."))

        if not username:
            raise TypeError("You must provide a user name.")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Creates a modified class based on AbstractBaseUser."""

    username = models.CharField(
        max_length=255,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'), db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    acc_hash = models.UUIDField(unique=True, default=uuid.uuid4)
    is_verified = models.BooleanField(
        default=False,
        help_text=_(
            'This user has verified their account after it has been created.'))
    is_active = models.BooleanField(
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),)
    is_staff = models.BooleanField(
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self) -> str:
        return self.username
