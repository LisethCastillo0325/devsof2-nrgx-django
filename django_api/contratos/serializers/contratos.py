"""Contratos serializers """

# Django REST Framework
from rest_framework import serializers

# Models
from ..models.contratos import Contratos

# Serializers
from django_api.users.serializers import ClienteModelSerializer
from django_api.utils.serializers import DataSerializer, DataChoiceSerializer


class ContratosSerializer(serializers.ModelSerializer):
    cliente = ClienteModelSerializer()
    ciudad = DataSerializer()
    tipo_de_uso = DataChoiceSerializer()
    estado = DataChoiceSerializer()
    estado_de_pago = DataChoiceSerializer()

    class Meta:
        model = Contratos
        fields = [
            'id', 'cliente', 'direccion_instalacion', 'ciudad', 'tipo_de_uso', 'estrato',
            'estado', 'estado_de_pago'
        ]