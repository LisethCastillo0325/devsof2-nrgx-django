""" Este código define una clase ContratosAdmin que extiende de admin.ModelAdmin. Se configura para 
personalizar la visualización de la lista de objetos de Contratos en la interfaz de administración de 
Django. Los campos que se muestran en la lista y los campos que se pueden usar para filtrar la lista se
 definen en las propiedades list_display y list_filter, respectivamente.

Finalmente, se registra el modelo de Contratos en el sitio de administración de Django utilizando 
admin.site.register() con la clase ContratosAdmin como segundo parámetro, lo que indica que se utilizará
 la configuración personalizada para la visualización de la lista de objetos de Contratos en la interfaz 
 de administración de Django."""


from django.contrib import admin

from .models.contratos import Contratos


class ContratosAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'ciudad', 'tipo_de_uso', 'estrato', 'estado', 'estado_de_pago')
    list_filter = ('cliente', 'ciudad', 'tipo_de_uso', 'estrato', 'estado', 'estado_de_pago')

# Register your models here.
admin.site.register(Contratos, ContratosAdmin)