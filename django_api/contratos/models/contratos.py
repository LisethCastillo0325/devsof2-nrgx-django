"""Contratos Model"""

# Django
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
    latitud = models.DecimalField('Latitud', max_digits=10, decimal_places=8)
    longitud = models.DecimalField(max_digits=10, decimal_places=8)
    ciudad = models.ForeignKey('utils.Ciudades', on_delete=models.CASCADE)
    tipo_de_uso = models.CharField(
        'Tipo de uso',
        choices=TipoDeUsoChoices.choices,
        max_length=1,
        default=TipoDeUsoChoices.RECIDENCIAL
    )
    estrato = models.IntegerField('Estrato socioeconomico')
    estado = models.CharField('Estado', choices=EstadoChoices.choices, max_length=1)
    estado_de_pago = models.CharField('Estado de pago', choices=EstadoDePago.choices, max_length=1)
    sericios = models.ManyToManyField('servicios.Servicios', related_name='servicios_contrato')

    def __str__(self):
        return "Contrato {}".format(self.id)

    class Meta(DateBaseModel.Meta):
        db_table = 'contratos'
        managed = True
        verbose_name = 'contrato'
        verbose_name_plural = 'contratos'

