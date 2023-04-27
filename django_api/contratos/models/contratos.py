"""Contratos Model"""

# Django

#Este código define un modelo de Django llamado "Contratos" que hereda 
# de una clase personalizada llamada "DateBaseModel". Esta clase se importa
# desde "django_api.utils.models" y proporciona campos de fecha y hora "created"
#  y "modified" para el modelo.
# 
# El modelo "Contratos" tiene los siguientes campos:
# 
# cliente: un campo de clave externa que se relaciona con el modelo "User".
# direccion_instalacion: un campo de texto que almacena la dirección de instalación.
# latitud: un campo decimal que almacena la latitud de la dirección de instalación.
# longitud: un campo decimal que almacena la longitud de la dirección de instalación.
# ciudad: un campo de clave externa que se relaciona con el modelo "Ciudades".
# tipo_de_uso: un campo de opción que indica si el contrato es para uso residencial o comercial.
# estrato: un campo entero que indica el estrato socioeconómico del cliente.
# estado: un campo de opción que indica si el contrato está activo, inactivo o suspendido.
# estado_de_pago: un campo de opción que indica si el contrato está al día o en mora.
# servicios: un campo ManyToMany que se relaciona con el modelo "Servicios".
# fecha_instalacion: un campo de fecha y hora que almacena la fecha y hora de la instalación.

#Y además, define tres clases anidadas:

#TipoDeUsoChoices: una clase que define las opciones de uso del contrato (residencial o comercial).
#EstadoChoices: una clase que define las opciones de estado del contrato (activo, inactivo o suspendido).
#EstadoDePago: una clase que define las opciones de estado de pago del contrato (al día o en mora).
#Finalmente, el modelo define un método "str" que devuelve una cadena que representa el objeto 
# "Contratos" y una clase "Meta" que define varios metadatos, como el nombre de la tabla de la base de
#  datos, si el modelo es gestionado por Django y los nombres plurales y singulares para el modelo en 
# la interfaz de administración de Django.

from django.db import models
from django.utils.translation import gettext_lazy as _

# Utilities
from django_api.utils.models import DateBaseModel


class Contratos(DateBaseModel):

    class TipoDeUsoChoices(models.TextChoices):
        RECIDENCIAL = 1
        COMERCIAL = 2

    class EstadoChoices(models.TextChoices):
        ACTIVO = 1
        INACTIVO = 2
        SUSPENDIDO = 3

    class EstadoDePago(models.TextChoices):
        ALDIA = 1, _('AL DÍA')
        ENMORA = 2, _('EN MORA')

    cliente = models.ForeignKey('users.User', on_delete=models.CASCADE)
    direccion_instalacion = models.CharField('Dirección de instalación', max_length=150)
    latitud = models.DecimalField('Latitud', max_digits=10, decimal_places=8, default=0)
    longitud = models.DecimalField('Longitud', max_digits=10, decimal_places=8, default=0)
    ciudad = models.ForeignKey('utils.Ciudades', on_delete=models.CASCADE)
    tipo_de_uso = models.CharField(
        'Tipo de uso',
        choices=TipoDeUsoChoices.choices,
        max_length=1,
        default=TipoDeUsoChoices.RECIDENCIAL
    )
    estrato = models.IntegerField('Estrato socioeconomico')
    estado = models.CharField('Estado', choices=EstadoChoices.choices, default=EstadoChoices.INACTIVO, max_length=1)
    estado_de_pago = models.CharField('Estado de pago', choices=EstadoDePago.choices, max_length=1, null=True)
    servicios = models.ManyToManyField('servicios.Servicios', related_name='servicios_contrato')
    fecha_instalacion = models.DateTimeField('Fecha de instalación', help_text="Fecha y hora de instalación")


    def __str__(self):
        return "Contrato {}".format(self.id)

    class Meta(DateBaseModel.Meta):
        db_table = 'contratos'
        managed = True
        verbose_name = 'contrato'
        verbose_name_plural = 'contratos'

