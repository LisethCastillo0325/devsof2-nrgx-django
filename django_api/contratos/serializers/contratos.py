"""Contratos serializers """

# Django REST Framework
from rest_framework import serializers

# Models
from ..models.contratos import Contratos
from django_api.users.models.users import User

# Serializers
from django_api.users.serializers import ClienteModelSerializer
from django_api.utils.serializers import DataSerializer, DataChoiceSerializer

# Constant
from django_api.users.constant import GroupsConstant


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


class ContratosModelSerializer(serializers.ModelSerializer):
    cliente = ClienteModelSerializer()
    ciudad = DataSerializer()
    tipo_de_uso = DataChoiceSerializer()
    estado = DataChoiceSerializer()
    estado_de_pago = DataChoiceSerializer()
    servicios = DataSerializer(many=True)

    class Meta:
        model = Contratos
        fields = ('__all__')


class UpdateAndCreatedContratoSerializer(serializers.ModelSerializer):
    cliente = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(groups__id__in=[GroupsConstant.CLIENTE])
    )
    estrato = serializers.IntegerField(min_value=1, max_value=6)

    class Meta:
        model = Contratos
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

