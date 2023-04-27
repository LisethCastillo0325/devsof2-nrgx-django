"""Factura model."""


""" 

Este código define tres modelos de Django para la gestión de facturas y detalles de facturas, junto con 
la configuración de facturación en un sistema.

El primer modelo, Facturas, representa una factura emitida para un contrato específico y contiene 
información como la fecha de expedición, la fecha de vencimiento, el número de pago electrónico, el 
estado actual de la factura (pagada, pendiente o inactiva), y los valores pendientes de pago y de 
recargo, si los hay.

El segundo modelo, DetalleFactura, representa los detalles específicos de una factura, como el servicio
 que se está facturando, la lectura anterior y actual del servicio, el consumo actual, el valor unitario
   del servicio, los cargos por recargo y el total a pagar por este detalle de factura.

El tercer modelo, ConfiguracionesFacturacion, contiene la información de configuración de la facturación,
 como el día de corte y el porcentaje de recargo por mora general que se aplicará en el sistema.

Todos los modelos heredan de la clase DateBaseModel, que proporciona campos de fecha y hora 
estandarizados para la creación y actualización de objetos. Además, el modelo Facturas utiliza la clase 
EstadoChoices para proporcionar opciones de estado predefinidas para las facturas.

"""
# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utilities
from django_api.utils.models import DateBaseModel


class Facturas(DateBaseModel):
    """Factura model.

    Facturación del servicios o servicios consumidos por un cliente
    """
    class EstadoChoices(models.TextChoices):
        PAGADA = 1,_('PAGADA')
        PENDIENTE = 2,_('PENDIENTE')
        INACTIVA = 3,_('INACTIVA')

    contrato = models.ForeignKey('contratos.Contratos', on_delete=models.CASCADE)
    fecha_expedicion = models.DateTimeField('Fecha de expedición')
    fecha_vencimiento = models.DateTimeField('Fecha de vencimiento')
    numero_pago_electronico = models.CharField(max_length=15)
    estado = models.CharField(max_length=1, choices=EstadoChoices.choices, default=EstadoChoices.PENDIENTE)
    valor_pendiente_pago = models.FloatField('Valor pendiente de pago', default=0)
    is_recargo = models.BooleanField(
        'Recargo',
        default=False,
        help_text=(
            'ayuda a saber si se le aplica recargo o no'
        )
    )
    valor_recargo = models.IntegerField('Valor de recargo', default=0)
    total_a_pagar = models.IntegerField('Total a pagar', default=0)

    def __str__(self):
        return "Factura {}".format(self.id)

    class Meta(DateBaseModel.Meta):
        db_table = 'facturas'
        managed = True
        verbose_name = 'factura'
        verbose_name_plural = 'facturas'


class DetalleFactura(DateBaseModel):

    factura = models.ForeignKey(Facturas, on_delete=models.CASCADE)
    servicio = models.ForeignKey('servicios.Servicios', on_delete=models.CASCADE)
    lectura_anterior = models.BigIntegerField('Lectura anterior')
    lectura_actual = models.BigIntegerField('Lectura actual')
    consumo_actual = models.IntegerField('Consumo actual')
    valor_unitario = models.FloatField('Valor unitario')
    valor_total = models.FloatField('Valor total')
    porcentaje_recargo = models.BigIntegerField('Porcentaje de cargo', default=0)
    valor_recargo = models.IntegerField('Valor de recargo', default=0)
    total_a_pagar = models.IntegerField('Total a pagar')

    def __str__(self):
        return "Detalle factura {}".format(self.factura_id)

    class Meta(DateBaseModel.Meta):
        db_table = 'detalle_factura'
        managed = True
        verbose_name = 'detalle_factura'
        verbose_name_plural = 'detalles de factura'


class ConfiguracionesFacturacion(DateBaseModel):

    dia_de_corte = models.IntegerField('Día de corte')
    porcentaje_recargo_mora = models.FloatField('Porcentaje de recargo por mora general')
    
    def __str__(self):
        return "ConfiguracionesFacturacion {}".format(self.id)

    class Meta(DateBaseModel.Meta):
            db_table = 'configuraciones_facturacion'
            managed = True
            verbose_name = 'configuraciones_facturacion'
            verbose_name_plural = 'configuraciones facturacion'