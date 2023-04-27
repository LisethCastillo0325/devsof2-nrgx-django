"""Factura app."""

""" Este código define la configuración de la aplicación "Contratos". Se utiliza la clase AppConfig 
de Django para configurar la aplicación y se especifica el nombre de la aplicación (name) y su nombre 
para ser mostrado en la interfaz de administración (verbose_name). En este caso, el nombre de la 
aplicación es django_api.contratos y su nombre para la interfaz de administración es "Contratos"."""


# Django
from django.apps import AppConfig

class ContratoAppConfig(AppConfig):
    """Contratos app config."""
    name = 'django_api.contratos'
    verbose_name = 'Contratos'