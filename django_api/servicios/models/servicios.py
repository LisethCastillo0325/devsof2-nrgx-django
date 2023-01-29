"""Servicios Model"""

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utilities
from django_api.utils.models import DateBaseModel


class Servicios(DateBaseModel):

    class UnidadMedidaChoices(models.TextChoices):
        KWH = 1, _('KILOVATIO HORA')
        MC = 2, _('METROS CÚBICOS')

    nombre = models.CharField('Nombre', max_length=150)
    descripcion = models.CharField('Descripción', max_length=250, null=True, blank=True)
    unidad_medida = models.CharField('Unidad de medida', choices=UnidadMedidaChoices.choices, max_length=1)
    valor_unitario = models.FloatField('Valor unitario')
    dia_de_corte = models.IntegerField('Día de corte')
    porcentaje_recargo_mora = models.FloatField('Porcentaje de recargo por mora')
    is_active = models.BooleanField('Estado', default=True)

    def __str__(self):
        return "Servicio ID: {} Nombre: {}".format(self.id, self.nombre)

    class Meta(DateBaseModel.Meta):
        db_table = 'servicios'
        managed = True
        verbose_name = 'servicio'
        verbose_name_plural = 'servicios'