from django.db import transaction

# Rest Framework
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from django_api.facturas.serializers.facturas_pagos import AddPagoFacturaSerializer

# Models
from ..models.facturas_pagos import PagosFactura

# Serializers
# from ..serializers import contratos as contratos_serialisers


class PagosFacturasViewSet(viewsets.GenericViewSet):

    queryset = PagosFactura.objects.all()
    # serializer_class = contratos_serialisers.ContratosModelSerializer
    permission_classes = [IsAuthenticated]
   

    @transaction.atomic
    @action(detail=False, methods=['POST'])
    def bancos(self, request, *args, **kwargs):

        # agregar logica de leer el archivo plano

        listado_pagos = [
            {
             "factura": 8938493,
             "user": 5,
            }
        ]

        for pago in listado_pagos:

            serializer = AddPagoFacturaSerializer(data=pago)
            serializer.is_valid(raise_exception=True)
            serializer.save()


        return Response(data={"detail": "Pagos creados."}, status=status.HTTP_201_CREATED) 



    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)
