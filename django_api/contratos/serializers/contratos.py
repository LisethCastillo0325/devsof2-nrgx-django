

"""Contratos serializers """

""" Este código define tres clases de serializadores para el modelo de Django "Contratos":

ContratosSerializer: serializador que muestra datos simplificados del contrato, incluyendo información 
del cliente, ciudad, tipo de uso, estrato, estado y estado de pago. Utiliza otros serializadores para 
mostrar información detallada del cliente, ciudad y elecciones de campos de texto.

ContratosModelSerializer: serializador que muestra todos los campos del modelo de Contratos. Además de 
los campos que muestra ContratosSerializer, también incluye la relación muchos a muchos con el modelo 
de Servicios y todos los campos de fecha y hora.

UpdateAndCreatedContratoSerializer: serializador que permite crear y actualizar instancias del modelo 
de Contratos. Además de todos los campos del modelo, también requiere un ID de cliente y un valor de 
estrato. El ID de cliente debe ser una clave externa a la tabla "User" con un grupo "CLIENTE", y el 
valor de estrato debe estar entre 1 y 6. Este serializador define las funciones create() y update() 
para procesar los datos validados y crear o actualizar instancias de Contratos según sea necesario."""

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

