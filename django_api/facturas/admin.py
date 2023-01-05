from django.contrib import admin

from .models.facturas import Facturas, DetalleFactura


class FacturasAdmin(admin.ModelAdmin):
    list_display = ('id', 'contrato', 'contrato', 'estado', 'valor_pendiente_pago', 'total_a_pagar')


class DetalleFacturaAdmin(admin.ModelAdmin):
    list_display = (
        'factura', 'servicio', 'lectura_anterior', 'lectura_actual', 
        'consumo_actual', 'valor_unitario', 'valor_total'
    )

# Register your models here.
admin.site.register(Facturas, FacturasAdmin)
admin.site.register(DetalleFactura, DetalleFacturaAdmin)