from django.contrib import admin

from .models.bancos import Bancos


class BancosAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'nombre', 'created'
    )

# Register your models here.
admin.site.register(Bancos, BancosAdmin)