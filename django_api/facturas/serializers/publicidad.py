"""Publicidad serializers """

# Django REST Framework
from rest_framework import serializers

# Models
from ..models.publicidad import Publicidad


class PublicidadModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Publicidad
        fields = ('__all__')


class UpdateAndCreatedPublicidadSerializer(serializers.ModelSerializer):
    seccion_factura = serializers.ChoiceField(
        choices=Publicidad.SeccionFacturaChoices.choices,
        default=Publicidad.SeccionFacturaChoices.SECCION_A
    )
    nombre = serializers.CharField(required=True)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Publicidad
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)