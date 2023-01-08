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
from django_api.servicios.models import Servicio
from django.contrib.auth.models import Group

# Utils
from django_api.utils.serializers import DataChoiceSerializer
from django.utils import timezone
#from datetime import timedelta
#from django_api.utils.custom_regex_validators import CellNumberRegexValidator


class ServicioModelSerializer(serializers.ModelSerializer):
    nombre= serializers.CharField()
    descripcion= serializers.CharField()

    class Meta:
        model = Servicio
        fields = [
            'id','nombre','descripcion','created','update','unidad_medida',
            'valor_unitario','dia_de_corte','porcentaje_recargo_mora','groups'
        ]

"""serializer dia de corte"""   

"""class dia_de_corte(serializers.Serializer):

    dia_de_corte= serializers.IntegerField()

    def validate(self, data):
        dia_de_corte = authenticate(dia_de_corte=data['Dia de corte'])
        if not dia_de_corte:
            raise serializers.ValidationError({'detail': 'Campo vacio'})
        self.context['dia de corte'] = dia_de_corte
        return super().validate(data)
    
    def create(self,validate_data):
        return self(**validate_data)"""


class UpdateAndCreateServicioSerializer(serializers.ModelSerializer):
    """
    Update and create servicio serializer.
    """
    nombre = serializers.CharField(max_length=150)
    descripcion = serializers.CharField(max_length=150)

    unidad_medida = serializers.ChoiceField(
        choices=Servicio.UnidadMedidaChoices.choices
    )
    valor_unitario = serializers.FloatField(required=False)
    porcentaje_recargo_mora = serializers.FloatField(min_length=6, max_length=30, required=False)
    
    # Relación m2m con la tabla de grupos, conocida tambien como "rol"
    groups = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        many=True
    )

    class Meta:
        """Meta class."""
        model = Servicio
        fields = '__all__'

    """def dia_de_corte_validate(self, dia_de_corte):
        dia_de_corte_validation.validate_dia(dia_de_corte=dia_de_corte)
        return dia_de_corte"""

    def create(self, data):
        """
        Crear servicios
        """
        groups_data = data.pop('groups')
        data['dia_de_corte'] = str(data.get('dia_de_corte', data['']))
        servicios = Servicio.objects.create(**data)
        servicios.set_dia_de_corte(data['dia_de_corte'])
        servicios.save()
        for group in groups_data:
            servicios.groups.add(group)
        return Servicio

    def update(self, instance, data):
        servicios = super().update(instance=instance, validated_data=data)
        try:
            servicios.set_dia_de_corte(data['dia_de_corte'])
            servicios.dia_de_corte_change_date = timezone.now()
            servicios.save()
        except KeyError:
            pass
        return Servicio



