from django.contrib import admin

from .models.facturas import Facturas, DetalleFactura
from .models.publicidad import Publicidad


class FacturasAdmin(admin.ModelAdmin):
    list_display = ('id', 'contrato', 'contrato', 'estado', 'valor_pendiente_pago', 'total_a_pagar', 'created')


class DetalleFacturaAdmin(admin.ModelAdmin):
    list_display = (
        'factura', 'servicio', 'lectura_anterior', 'lectura_actual', 
        'consumo_actual', 'valor_unitario', 'valor_total', 'created'
    )

class PublicidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_vigencia_inicio', 'fecha_vigencia_fin', 'valor', 'seccion_factura', 'imagen')

# Register your models here.
admin.site.register(Facturas, FacturasAdmin)
admin.site.register(DetalleFactura, DetalleFacturaAdmin)
admin.site.register(Publicidad, PublicidadAdmin)