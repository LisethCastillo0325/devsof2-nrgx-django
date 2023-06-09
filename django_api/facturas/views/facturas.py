import os
from django.utils import timezone
from django.conf import settings
from django.db import transaction

# Rest Framework
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..filter import FaturasViewFilter

# Models
from ..models.facturas import Facturas
from ..models.publicidad import Publicidad

# Serializers
from ..serializers import facturas as facturas_serialisers

# Views
from django_api.utils.views.documentos import DocumentosView

# Service
from django_api.facturas.services.factura import FacturaServices


class FacturasViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):

    queryset = Facturas.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['contrato__cliente__identification_number']
    ordering_fields = ['contrato__cliente']
    filterset_class = FaturasViewFilter

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action == 'create':
            return facturas_serialisers.AddFacturaSerializer
        return facturas_serialisers.FacturasModelSerializer

    def get_object(self):
        obj = get_object_or_404(self.get_queryset().exclude(
            estado=Facturas.EstadoChoices.INACTIVA), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

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

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """ Crear factura para un contrato

            Dado un contrato se crea su factura respectiva.
        """
        serializer = facturas_serialisers.AddFacturaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Crear factura al contrato
        factura = serializer.save()
        
        data = facturas_serialisers.FacturasModelSerializer(instance=factura).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    @action(detail=False, methods=['GET'])
    def crear_facturas_contratos(self, request, *args, **kwargs):
        """ Crear factura a todos los contratos 

            Por cada contrato se crea su respectiva factura.
        """
        service = FacturaServices()
        facturas = service.crear_facturas_contratos()

        data = facturas_serialisers.FacturasModelSerializer(
            instance=facturas, many=True).data
            
        return Response(data=data, status=status.HTTP_201_CREATED)
        
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
        """ Descargar Factura PDF

            Dado un ID de factura permite descargar su representación en PDF.
        """

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
        