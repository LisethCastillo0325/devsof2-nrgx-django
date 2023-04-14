""" Facturas serializers """

# Django REST Framework
from rest_framework import serializers

from ..models.facturas import Facturas
from django_api.users.models.users import User
from django_api.bancos.models.bancos import Bancos
from ..models.facturas_pagos import PagosFactura


class AddPagoFacturaSerializer(serializers.Serializer):
    
    factura = serializers.PrimaryKeyRelatedField(
        queryset=Facturas.objects.all()
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    total_pago = serializers.FloatField()
    forma_pago = serializers.ChoiceField(
        choices=PagosFactura.FormaPagoChoices.choices
    )
    banco = serializers.PrimaryKeyRelatedField(
        queryset=Bancos.objects.all(), required=False
    )


    def create(self, validated_data):
        
        pago = PagosFactura.objects.create(
            **validated_data
        )

        # agregar logica adicional o necesaria

        # es similar a hacer esto
        # pago = PagosFactura.objects.create(
        #     factura=validated_data['factura'],
        #     user=validated_data['user'],
        #     total_pago=validated_data['total_pago'],
        # )

        return pago


class AddPagoFacturaBancosSerializer(AddPagoFacturaSerializer):
    # Se pide como obligatorio el banco
    banco = serializers.PrimaryKeyRelatedField(
        queryset=Bancos.objects.all(), required=True
    )
