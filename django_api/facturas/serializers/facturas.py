""" Facturas serializers """

# Django REST Framework
from rest_framework import serializers

# Models
from django_api.facturas.models import Facturas, DetalleFactura

# Serializers
from django_api.contratos.serializers.contratos import ContratosModelSerializer
from django_api.utils.serializers import  DataChoiceSerializer, DataSerializer


class DetalleFacturaModelSerializer(serializers.ModelSerializer):
    servicio = DataSerializer()

    class Meta:
        model = DetalleFactura
        fields = ('__all__')


class FacturasModelSerializer(serializers.ModelSerializer):
    contrato = ContratosModelSerializer()
    estado = DataChoiceSerializer()
    detalle_factura = serializers.SerializerMethodField()

    def get_detalle_factura(self, obj):
        try:
            queryset = DetalleFactura.objects.filter(factura_id=obj.id)
            return DetalleFacturaModelSerializer(instance=queryset, many=True).data
        except Exception:
            return None
    
    class Meta:
        model = Facturas
        fields = ('__all__')


