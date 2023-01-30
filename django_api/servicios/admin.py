from django.contrib import admin

from .models.servicios import Servicios, LogConsumoServicios


class ServiciosAdmin(admin.ModelAdmin):
    list_display = (
        'nombre', 'descripcion', 'unidad_medida', 'valor_unitario', 
        'porcentaje_recargo_mora'
    )
    list_filter = ('unidad_medida',)


class LogConsumoServiciosAdmin(admin.ModelAdmin):
    list_display = ('factura', 'servicio', 'lectura')


# Register your models here.
admin.site.register(Servicios, ServiciosAdmin)
admin.site.register(LogConsumoServicios, LogConsumoServiciosAdmin)