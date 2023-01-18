"""Users model admin."""

# Dajngo
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from django_api.users.models import User


class CustomUserAdmin(UserAdmin):

    # Lista de campos a mostrar en la tabla principal
    list_display = (
        'email', 'first_name', 'last_name', 'identification_number', 'identification_type', 
        'is_active', 'is_client', 'is_staff'
    )

    # Campos que determinan el orden del resultado
    ordering = ('is_active',)

    # Campos de busqueda
    search_fields = ("first_name", "last_name", "email")

    # Campos del formulario de USUARIO en secciones (update)
    fieldsets = (
        ('CREDENCIALES', {
            'fields': ('email', 'password')
        }),
        ('INFORMACIÓN BASICA', {
            'fields': (
                'identification_number', 'identification_type', 'first_name', 'last_name', 'phone_number',
                'birth_date'
            )
        }),
        ('INFORMACIÓN DEL USARIO', {
            'fields': ('groups', 'is_active', 'is_client')
        }),
    )

    # Campos del formulario de USUARIO en secciones (create)
    add_fieldsets = (
        ('CREDENCIALES', {
            'fields': ('email', 'password1', 'password2')
        }),
        ('INFORMACIÓN BASICA', {
            'fields': (
                'identification_number', 'identification_type', 'first_name', 'last_name', 'phone_number', 
                'birth_date', 'date_joined',
            )
        }),
        ('INFORMACIÓN DEL USARIO', {
            'fields': ('groups', 'is_client'),
        }),
    )

admin.site.register(User, CustomUserAdmin)