from django.contrib import admin

from .models.contratos import Contratos


class ContratosAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'ciudad', 'tipo_de_uso', 'estrato', 'estado', 'estado_de_pago')
    list_filter = ('cliente', 'ciudad', 'tipo_de_uso', 'estrato', 'estado', 'estado_de_pago')

# Register your models here.
admin.site.register(Contratos, ContratosAdmin)