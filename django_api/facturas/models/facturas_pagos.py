# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utilities
from django_api.utils.models import DateBaseModel

class PagosFactura(DateBaseModel):

    class FormaPagoChoices(models.TextChoices):
        PRESECIAL = 1, _('PRESECIAL')
        BANCO = 2, _('BANCO')
        VIRTUAL = 3, _('VIRTUAL')

    factura = models.ForeignKey('facturas.Facturas', on_delete=models.CASCADE)
    banco = models.ForeignKey('bancos.Bancos', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    forma_pago = models.CharField('Forma de pago', choices=FormaPagoChoices.choices, max_length=1)
    total_pago = models.FloatField('Total de pago')
    
    def __str__(self):
        return "Pagos id {} factura {}".format(self.id, self.factura_id)

    class Meta(DateBaseModel.Meta):
        db_table = 'pagos_factura'
        managed = True
        verbose_name = 'pagos_factura'
        verbose_name_plural = 'pagos de facturas'