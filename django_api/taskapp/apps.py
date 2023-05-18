"""Factura app."""

# Django
from django.apps import AppConfig

class CeleryAppConfig(AppConfig):
    """Celery app config."""
    name = 'django_api.taskapp'
    verbose_name = 'Celery App'