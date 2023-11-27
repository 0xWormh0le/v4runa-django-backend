from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from common.fields import NormalizedEmailField
from .constants import (
    USER_ROLE_CHOICES,
    ROLE_ADMIN,
    ROLE_GENERAL_MANAGER,
    ROLE_OPERATION_MANAGER,
    ROLE_CUSTOMER,
)


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('username', email)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('username', email)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = NormalizedEmailField(unique=True)
    role = models.IntegerField(choices=USER_ROLE_CHOICES, default=ROLE_ADMIN)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @cached_property
    def is_admin(self):
        return self.role == ROLE_ADMIN

    @cached_property
    def is_general_manager(self):
        return self.role == ROLE_GENERAL_MANAGER

    @cached_property
    def is_operation_manager(self):
        return self.role == ROLE_OPERATION_MANAGER

    @cached_property
    def is_consumer(self):
        return self.role == ROLE_CONSUMER

    def __str__(self):
        return self.email


class NewSignup(User):
    class Meta:
        proxy = True


class Profile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    water_utility = models.ForeignKey(
        'utility.WaterUtility',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    is_approved = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=12)
    subscribe_desc = models.TextField(
        max_length=1024,
        help_text='User left text when he signed up',
        blank=True
    )

    def __str__(self):
        return str(self.user)


class Memo(models.Model):
    memo = models.TextField(
        max_length=4096,
        help_text='Memo',
        blank=True)

    email_domain = models.TextField(
        max_length=32,
        blank=False,
        default='',
        help_text='Email domain')

    def __str__(self):
        return str(self.memo)
