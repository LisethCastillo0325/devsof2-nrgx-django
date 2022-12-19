"""Users model admin."""

# Dajngo
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from django_api.users.models import User


class CustomUserAdmin(UserAdmin):

    list_display = (
        'email', 'first_name', 'last_name', 'identification_number', 'identification_type', 
        'is_active', 'is_client', 'is_staff'
    )
    list_filter = ('identification_number', 'is_staff', 'is_active', 'created', 'updated')

    ordering = ('is_active',)

admin.site.register(User, CustomUserAdmin)