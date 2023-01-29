# Rest Framework
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Models
from ..models.contratos import Contratos

# Serializers
from ..serializers import contratos as contratos_serialisers


class ContratosViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):

    queryset = Contratos.objects.all()
    serializer_class = contratos_serialisers.ContratosModelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['direccion_instalacion']
    ordering_fields = ['cliente']
    filter_fields = ('cliente', 'ciudad', 'tipo_de_uso', 'estado', 'estado_de_pago', 'servicios')

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action in ['update', 'partial_update', 'create']:
            return contratos_serialisers.UpdateAndCreatedContratoSerializer
        return contratos_serialisers.ContratosModelSerializer

    def list(self, request, *args, **kwargs):
        """ Listar contratos

            Permite listar todos los contratos registrados en el sistema.
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """ Consultar contrato por ID

            Permite obtener información de un contrato dado su ID
        """  
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """ Crear contrato

            Permite crear un contrato de servicios a un cliente
        """
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """ Editar contrato

            Permite editar un contrato de servicios a un cliente
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """ Edición parcial de contrato

            Permite editar parcialmente un contrato de servicios a un cliente
        """
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """ Inactivar contrato

            Permite inactivar un contrato, no lo elimina.
        """
        return super().destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        """Metodo invocado por 'destroy' para cambiar el estado del Contrato."""
        instance.estado = Contratos.EstadoChoices.INACTIVO
        instance.save()
