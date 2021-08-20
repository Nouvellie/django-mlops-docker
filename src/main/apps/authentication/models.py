from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self, email, username, password, **other_fields):

        if not email:
            raise ValueError(_("You must provide an email address."))

        if not username:
            raise TypeError("You must provide a user name.")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_verified', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        if other_fields.get('is_verified') is not True:
            raise ValueError(
                'Superuser must be assigned to is_verified=True.')

        return self.create_user(email, username, password, **other_fields)

    def create_staffuser(self, email, username, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', False)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_verified', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Staffuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not False:
            raise ValueError(
                'Staffuser must be assigned to is_superuser=False.')
        if other_fields.get('is_verified') is not True:
            raise ValueError(
                'Staffuser must be assigned to is_verified=True.')

        return self.create_user(email, username, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        max_length=255,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'), db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_verified = models.BooleanField(default=False)
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

    def __str__(self):
        return f"User '{self.username}' with email '{self.email}'."

    def token(self):
        return ''
