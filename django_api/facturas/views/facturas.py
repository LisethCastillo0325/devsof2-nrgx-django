import os

# Rest Framework
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Models
from ..models.facturas import Facturas

# Serializers
from ..serializers import facturas as facturas_serialisers

# Views
from django_api.utils.views.documentos import DocumentosView


class FacturasViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):

    queryset = Facturas.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['contrato__cliente__identification_number']
    ordering_fields = ['contrato__cliente']
    filter_fields = (
        'contrato', 'contrato__cliente', 'contrato__cliente__identification_number',
        'estado', 'is_recargo', 'numero_pago_electronico', 'fecha_expedicion', 'fecha_vencimiento'
    )

    def get_serializer_class(self):
        """Return serializer based on action."""
        return facturas_serialisers.FacturasModelSerializer

    def list(self, request, *args, **kwargs):
        """ Listar facturas

            Permite listar todos los facturas registradas en el sistema.
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """ Consultar factura por ID

            Permite obtener información de un factura dado su ID
        """  
        return super().retrieve(request, *args, **kwargs)


    def destroy(self, request, *args, **kwargs):
        """ Inactivar factura

            Permite anular una factura, no lo elimina.
        """
        return super().destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        """Metodo invocado por 'destroy' para cambiar el estado del Contrato."""
        instance.estado = Facturas.EstadoChoices.INACTIVA
        instance.save()


    @action(detail=True, methods=['GET'])
    def descargar(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.get_serializer(instance=instance).data

        template = os.path.join('documentos', 'factura.html')

        documentos_view = DocumentosView()
        return documentos_view.generar_pdf(
            template=template,
            data=data,
            file_name='factura_{}_{}'.format(instance.id, instance.contrato.cliente.identification_number)
        )
        