# Rest Framework
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Models
from ..models.facturas import ConfiguracionesFacturacion

# Serializers
from ..serializers import configuraciones_factura as configuraciones_facturacion_serialisers


class ConfiguracionesFacturacionViewSet(mixins.ListModelMixin,
                                        mixins.CreateModelMixin,
                                        mixins.UpdateModelMixin,
                                        mixins.RetrieveModelMixin,
                                        viewsets.GenericViewSet):

    queryset = ConfiguracionesFacturacion.objects.all()
    serializer_class = configuraciones_facturacion_serialisers.ConfiguracionesFacturacionModelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('dia_de_corte', 'porcentaje_recargo_mora')

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action in ['update', 'partial_update', 'create']:
            return configuraciones_facturacion_serialisers.UpdateAndCreatedConfiguracionesFacturacionSerializer
        return configuraciones_facturacion_serialisers.ConfiguracionesFacturacionModelSerializer

    def list(self, request, *args, **kwargs):
        """ Listar configuraciones facturación

            Permite listar todos los configuraciones facturacion registradas en el sistema.
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """ Consultar configuraciones facturacion por ID

            Permite obtener información la configuración facturación dado su ID
        """  
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """ Crear configuraciones facturación

            Permite crear un configuraciones facturación de servicios a un cliente
        """
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """ Editar configuraciones facturacion

            Permite editar un configuraciones facturación de servicios a un cliente
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """ Edición parcial de configuraciones facturacion

            Permite editar parcialmente un configuraciones facturación de servicios a un cliente
        """
        return super().partial_update(request, *args, **kwargs)
