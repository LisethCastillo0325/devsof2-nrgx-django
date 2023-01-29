"""Publicidad model."""

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utilities
from django_api.utils.models import DateBaseModel

class Publicidad(DateBaseModel):
    
    class SeccionFacturaChoices(models.TextChoices):
        SECCION_A = 'A'
        SECCION_B = 'B'
        SECCION_C = 'C'

    fecha_vigencia_inicio = models.DateTimeField('Fecha inicio de vigencia')
    fecha_vigencia_fin = models.DateTimeField('Fecha fin de vigencia')
    valor = models.FloatField('Valor', help_text="Valor pagado por la publicidad", default=0)
    imagen = models.ImageField('Imagen', upload_to ='uploads/publicidad/')
    seccion_factura = models.CharField(
        'Seccion Factura',
        choices=SeccionFacturaChoices.choices,
        max_length=1,
        default=SeccionFacturaChoices.SECCION_A
    )

    def __str__(self):
        return "Publicidad {}".format(self.id)

    class Meta(DateBaseModel.Meta):
        db_table = 'publicidad'
        managed = True
        verbose_name = 'publicidad'
        verbose_name_plural = 'publicidades'