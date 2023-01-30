import os
from django.utils import timezone
from django.conf import settings

# Rest Framework
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Models
from ..models.facturas import Facturas
from ..models.publicidad import Publicidad

# Serializers
from ..serializers import facturas as facturas_serialisers
from ..serializers.publicidad import PublicidadModelSerializer

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

        # Consultar publicidad vigente
        hoy = timezone.now()
        filtros_publicidad = {
            'fecha_vigencia_inicio__lte': hoy,
            'fecha_vigencia_fin__gte': hoy,
            'is_active': True,
        }

        publicidad_seccion_a = Publicidad.objects.filter(
            **filtros_publicidad,
            seccion_factura=Publicidad.SeccionFacturaChoices.SECCION_A
        ).first()

        publicidad_seccion_b = Publicidad.objects.filter(
            **filtros_publicidad,
            seccion_factura=Publicidad.SeccionFacturaChoices.SECCION_B
        ).first()

        publicidad_seccion_c = Publicidad.objects.filter(
            **filtros_publicidad,
            seccion_factura=Publicidad.SeccionFacturaChoices.SECCION_C
        ).first()

        publicidad_otros = Publicidad.objects.filter(
            **filtros_publicidad,
            seccion_factura=Publicidad.SeccionFacturaChoices.OTRO
        )

        data['publicidad_seccion_a'] = publicidad_seccion_a
        data['publicidad_seccion_b'] = publicidad_seccion_b
        data['publicidad_seccion_c'] = publicidad_seccion_c
        data['publicidad_otros'] = publicidad_otros
        data['url_api'] = settings.URL_BACKEND

        template = os.path.join('documentos', 'factura.html')
        documentos_view = DocumentosView()
        
        return documentos_view.generar_pdf(
            template=template,
            data=data,
            file_name='factura_{}_{}'.format(instance.id, instance.contrato.cliente.identification_number)
        )
        