"""factura model."""

# Django
from django.db import models


# Utilities
from django_api.utils.models import DateBaseModel

class Factura(DateBaseModel):
    """User model.
    
    Extend from Django's Abstract User, change the username field
    to email and add some extra fields.
    """
    class Estado(models.TextChoices):
        Pagado=1, ('La factura esta al dia')
        Pendiente= 2, ('La factura aun esta pendiente')

    fecha_expedicion= models.DateField(
        'Fecha de expedcion'
    )

    fecha_vencimiento = models.DateField(
        'Fecha de vencimiento'
    )

    total_pago = models.IntegerField(
        'Total a pagar',
        max_length= 20
    )

    valor_pendiente_pago = models.IntegerField(
        'Valor pendiente de pago',
        max_length=20
    )

    porcentaje_pago = models.BigIntegerField(
        'Porcentaje de pago',
        max_length=any
    )
    valor_recargo = models.IntegerField(
        'Valor de recargo',
        max_length= 20
    )

    recargo = models.BooleanField(
        'Recargo',
        default= False,
        help_text=(
            'ayuda a saber si se le aplica recargo o no'
        )
    )




    def __str__(self):
        return self.id  

    class Meta(DateBaseModel.Meta):
        db_table = 'factura'
        managed = True
        verbose_name = 'factura'
        verbose_name_plural = 'facturas'