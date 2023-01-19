""" Reporte clientes serializer """

# Django REST Framework
from rest_framework import serializers

# Models
from django_api.facturas.models import Facturas

# Serializers
from django_api.contratos.serializers.contratos import ContratosSerializer
from django_api.utils.serializers import  DataChoiceSerializer


class ReporteFacturasClientesSerializer(serializers.ModelSerializer):
    contrato = ContratosSerializer()
    estado = DataChoiceSerializer()
    
    class Meta:
        model = Facturas
        fields = [
            'id', 'contrato', 'valor_pendiente_pago', 'estado', 
            'is_recargo', 'porcentaje_recargo', 'valor_recargo', 'total_a_pagar'
        ]

class FiltrosReporteFacturasClientesSerializer(serializers.Serializer):
    created__gte = serializers.DateField(required=False)
    created__lte = serializers.DateField(required=False)
    clientes = serializers.CharField(required=False)
    contratos = serializers.CharField(required=False)
