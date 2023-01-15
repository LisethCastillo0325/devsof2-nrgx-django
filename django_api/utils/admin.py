from django.contrib import admin

from .models.ciudades import Ciudades 
from .models.departamentos import Departamentos


class CiudadesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'departamento')
    list_filter = ('departamento', )


class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

# Register your models here.
admin.site.register(Ciudades, CiudadesAdmin)
admin.site.register(Departamentos, DepartamentoAdmin) 