"""Development settings."""

from datetime import timedelta
from .base import *  # NOQA
from .base import env

# Base
DEBUG = True

PRODUCTION = False

# Security
SECRET_KEY = env('DJANGO_SECRET_KEY', default='django-insecure-tyx*dern6%a(xr&agj#31a&e=^@8q9dr-f)qm^t58*@$dh9hc$')
ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
    "3.20.82.253",
    "nrgx.tortascrispan.com"
]

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# Templates
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # NOQA

# Email
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

# django-extensions
INSTALLED_APPS += ['django_extensions']  # noqa F405

# JWT
# ------------------------------------------------------------------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=6),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# URL FRONTEND
# ------------------------------------------------------------------------------
URL_FRONTEND = 'http://localhost:3000'
