# Rest Framework
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Models
from ..models.publicidad import SeccionFactura

# Serializers
from ..serializers import publicidad as publicidad_serialisers


class SeccionFacturaViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):

    queryset = SeccionFactura.objects.all()
    serializer_class = publicidad_serialisers.SeccionFacturaModelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['seccion_factura']


    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action in ['update', 'partial_update', 'create']:
            return publicidad_serialisers.UpdateAndCreatedSeccionFacturaSerializer
        return publicidad_serialisers.SeccionFacturaModelSerializer

    def list(self, request, *args, **kwargs):
        """ Listar seccion factura

            Permite listar todas las seccion facturas registradas en el sistema.
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """ Consultar seccion factura por ID

            Permite obtener información de un seccion factura dado su ID
        """  
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """ Crear seccion factura

            Permite crear un seccion factura 
        """
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """ Editar seccion factura

            Permite editar un seccion factura 
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """ Edición parcial de seccion factura

            Permite editar parcialmente un seccion factura 
        """
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """ Inactivar seccion factura

            Permite eliminar un seccion factura
        """
        return super().destroy(request, *args, **kwargs)
