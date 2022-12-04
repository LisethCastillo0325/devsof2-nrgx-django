"""User model."""

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

# Utilities
from django_api.utils.models import DateBaseModel


class User(DateBaseModel, AbstractUser):
    """User model.
    
    Extend from Django's Abstract User, change the username field
    to email and add some extra fields.
    """

    class IdentificationTypeChoices(models.TextChoices):
        CC = 1, _('CÉDULA DE CIUDADANíA')
        CE = 2, _('CÉDULA DE EXTRANGERIA')
        NIT = 3, _('NÚMERO DE IDENTIFICACIÓN TRIBUTARIA')

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists'
        }
    )

    phone_number = models.CharField(max_length=10, blank=True)
    identification_number = models.BigIntegerField()
    identification_type = models.CharField(
        choices=IdentificationTypeChoices.choices,
        default=IdentificationTypeChoices.CC,
        max_length=1, null=True, blank=True
    )
    birth_date = models.DateField(null=True)

    is_client = models.BooleanField(
        'client',
        default=False,
        help_text=(
            'Help easily distinguis users and perform queries.'
        )
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name', 
        'last_name', 
        'username',
        'identification_number', 
        'identification_type'
    ]

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.email