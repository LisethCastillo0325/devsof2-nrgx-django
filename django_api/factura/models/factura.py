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
    estado = models.BooleanField(
        'Estado',
        default=True,
        help_text=(
            'Ayuda a saber si la factura esta activa o inactiva'
        )
    )
    def __str__(self):
        return self.id  

    class Meta(DateBaseModel.Meta):
        db_table = 'factura'
        managed = True
        verbose_name = 'factura'
        verbose_name_plural = 'facturas'