"""Servicios serializers."""

# Django
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.signals import user_logged_in

# Django REST Framework
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

# Models
from django_api.servicios.models import Servicio
from django.contrib.auth.models import Group

# Utils
from django_api.utils.serializers import DataChoiceSerializer
from django.utils import timezone
from datetime import timedelta
from django_api.utils.custom_regex_validators import CellNumberRegexValidator


class ServicioModelSerializer(serializers.ModelSerializer):
    nombre= serializers.CharField()
    descripcion= serializers.CharField()

    class Meta:
        model = Servicio
        fields = [
            '__all__'
        ]

"""serializer dia de corte"""   

class dia_de_corte(serializers.Serializer):

    dia_de_corte= serializers.IntegerField()

    def validate(self, data):
        dia_de_corte = authenticate(dia_de_corte=data['Dia de corte'])
        if not dia_de_corte:
            raise serializers.ValidationError({'detail': 'Campo vacio'})
        self.context['dia de corte'] = dia_de_corte
        return super().validate(data)
    
    def create(self,validate_data):
        return self(**validate_data)



