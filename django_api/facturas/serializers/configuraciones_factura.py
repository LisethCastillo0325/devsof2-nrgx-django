""" Facturas serializers """

# Django REST Framework
from rest_framework import serializers

# Models
from django_api.facturas.models import ConfiguracionesFacturacion

# Exceptions
from django_api.utils.exceptions import CustomValidationAPIException


class ConfiguracionesFacturacionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConfiguracionesFacturacion
        fields = ('__all__')


class UpdateAndCreatedConfiguracionesFacturacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConfiguracionesFacturacion
        fields = '__all__'

    def create(self, validated_data):
        qs = ConfiguracionesFacturacion.objects.all()
        if qs.count() > 0:
            raise CustomValidationAPIException({'detail': 'Ya existe una configuración creada por favor consultela.'})
        else:
            return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)