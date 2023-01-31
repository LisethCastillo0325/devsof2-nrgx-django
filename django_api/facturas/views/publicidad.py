# Rest Framework
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..filter import PublicidadFilter

# Models
from ..models.publicidad import Publicidad

# Serializers
from ..serializers import publicidad as publicidad_serialisers


class PublicidadViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):

    queryset = Publicidad.objects.all()
    serializer_class = publicidad_serialisers.PublicidadModelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombre']
    ordering_fields = ['fecha_vigencia_inicio']
    filterset_class = PublicidadFilter

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action in ['update', 'partial_update', 'create']:
            return publicidad_serialisers.UpdateAndCreatedPublicidadSerializer
        return publicidad_serialisers.PublicidadModelSerializer

    def list(self, request, *args, **kwargs):
        """ Listar publicidad

            Permite listar todas las publicidades registradas en el sistema.
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """ Consultar publicidad por ID

            Permite obtener información de un publicidad dado su ID
        """  
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """ Crear publicidad

            Permite crear un publicidad 
        """
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """ Editar publicidad

            Permite editar un publicidad 
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """ Edición parcial de publicidad

            Permite editar parcialmente un publicidad 
        """
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """ Inactivar publicidad

            Permite inactivar un publicidad, no lo elimina.
        """
        return super().destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        """Metodo invocado por 'destroy' para cambiar el estado del Contrato."""
        instance.is_active = False
        instance.save()
