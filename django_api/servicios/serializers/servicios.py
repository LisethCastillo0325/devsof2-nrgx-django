"""Servicios serializers."""

# Django
#from django.contrib.auth import authenticate, password_validation
#from django.contrib.auth.signals import user_logged_in

# Django REST Framework
from rest_framework import serializers
#from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
#from rest_framework_simplejwt.tokens import RefreshToken, TokenError

# Models
from django_api.servicios.models.servicios import Servicios
from django.contrib.auth.models import Group

# Utils
from django_api.utils.serializers import DataChoiceSerializer
from django.utils import timezone
#from datetime import timedelta
#from django_api.utils.custom_regex_validators import CellNumberRegexValidator


class ServicioModelSerializer(serializers.ModelSerializer):
    unidad_medida=DataChoiceSerializer()
    class Meta:
        model = Servicios
        fields = [
            'id','nombre','descripcion','created','updated','unidad_medida',
            'valor_unitario','dia_de_corte','porcentaje_recargo_mora', 'is_active'
        ]

class UpdateAndCreateServicioSerializer(serializers.ModelSerializer):
    """
    Update and create servicio serializer.
    """
    nombre = serializers.CharField(max_length=150)
    descripcion = serializers.CharField(max_length=150)
    dia_de_corte= serializers.IntegerField(min_value=1, max_value=30)

    unidad_medida = serializers.ChoiceField(
        choices=Servicios.UnidadMedidaChoices.choices
    )
    valor_unitario = serializers.FloatField()
    porcentaje_recargo_mora = serializers.FloatField()
    is_active = serializers.BooleanField(default=True)
    

    class Meta:
        """Meta class."""
        model = Servicios
        fields = '__all__'

    """def dia_de_corte_validate(self, dia_de_corte):
        dia_de_corte_validation.validate_dia(dia_de_corte=dia_de_corte)
        return dia_de_corte"""

    def create(self, data):
        """
        Crear servicios
        """
        servicios = Servicios.objects.create(**data)
        return servicios

    def update(self, instance, data):
        servicios = super().update(instance=instance, validated_data=data)
        
        return servicios



