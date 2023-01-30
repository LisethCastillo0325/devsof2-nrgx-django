from django.contrib import admin

from .models.facturas import Facturas, DetalleFactura, ConfiguracionesFacturacion
from .models.publicidad import Publicidad


class FacturasAdmin(admin.ModelAdmin):
    list_display = ('id', 'contrato', 'estado', 'valor_pendiente_pago', 'total_a_pagar', 'created')


class DetalleFacturaAdmin(admin.ModelAdmin):
    list_display = (
        'factura', 'servicio', 'lectura_anterior', 'lectura_actual', 
        'consumo_actual', 'valor_unitario', 'valor_total', 'created'
    )

class PublicidadAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'fecha_vigencia_inicio', 'fecha_vigencia_fin', 'valor', 
        'seccion_factura', 'imagen', 'is_active'
    )
    list_filter = ('is_active', 'seccion_factura')
    ordering = ['seccion_factura']

class ConfiguracionesFacturacionAdmin(admin.ModelAdmin):
    list_display = ('dia_de_corte', 'porcentaje_recargo_mora')

# Register your models here.
admin.site.register(Facturas, FacturasAdmin)
admin.site.register(DetalleFactura, DetalleFacturaAdmin)
admin.site.register(Publicidad, PublicidadAdmin)
admin.site.register(ConfiguracionesFacturacion)