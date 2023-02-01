"""Reportes Clientes."""

# Django REST Framework
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from django_api.facturas.models import Facturas

# Serializers
from ..serializers.clientes import ReporteFacturasClientesSerializer, FiltrosReporteFacturasClientesSerializer

# Filters
from django_api.facturas.filter import FaturasFilter


class ReportesClientesViewSet(viewsets.GenericViewSet):
    
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def informacion_financiera(self, request, **kwargs):
        """ Información financiera de clientes

            Reporte de información financiera de los clientes registrados en el sistema.
        """

        qs = Facturas.objects.select_related('contrato', 'contrato__cliente').all()
        serializer = FiltrosReporteFacturasClientesSerializer(
            data=request.GET,
        )
        serializer.is_valid(raise_exception=True)
        filters = serializer.data
        qs = FaturasFilter(filters, queryset=qs).qs

        if not qs.exists():
            return Response(data={
                'detail': 'No existen datos entre las fechas {} y {}.'.format(
                    filters['created__gte'], filters['created__lte'])
            }, status=status.HTTP_404_NOT_FOUND)

        else:
            data = ReporteFacturasClientesSerializer(instance=qs, many=True).data
            return Response(data=data, status=status.HTTP_200_OK)