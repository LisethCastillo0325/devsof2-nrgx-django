from django.db import transaction

# Rest Framework
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from django_api.facturas.serializers import facturas_pagos 
from django_api.utils.utils.upload_csv_excel import UploadCsvExcel

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

        # logica de leer el archivo plano
        parametros = {
            'data': request.data,
            'header': 0,
            'usecols': [0, 1, 2], # columnas en el archivo
            'names': ['factura', 'total_pago', 'banco']  # nombre de las columnas numeradas arriba
        }
        upload_csv_excel = UploadCsvExcel(**parametros)
        data_frame = upload_csv_excel.upload_file()
        listado_pagos = data_frame.to_dict('records')  # la información del archivo se transforma en una lista de diccionarios

        # Registrar los datos leídos
        for pago in listado_pagos:

            pago['user'] = request.user.id  # ID de usuario de sesión
            pago['forma_pago'] = PagosFactura.FormaPagoChoices.BANCO  # Por defecto es Banco

            serializer = facturas_pagos.AddPagoFacturaBancosSerializer(data=pago)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(data={"detail": "Pagos creados."}, status=status.HTTP_201_CREATED) 

    def create(self, request, *args, **kwargs):
        serializer = facturas_pagos.AddPagoFacturaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data={"detail": "Pago creado."}, status=status.HTTP_201_CREATED) 
