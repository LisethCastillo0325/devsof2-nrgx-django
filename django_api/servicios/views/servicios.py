"""Views servicio."""
# Django
from django.utils.decorators import method_decorator

# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

# Swagger
from drf_yasg.utils import swagger_auto_schema

# Models
from django_api.servicios.models import Servicios
# Serializers
from django_api.servicios import serializers


@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    auto_schema=None
))
class ServicioViewSet(mixins.ListModelMixin, 
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    """
    API de servicios
    """

    queryset = Servicios.objects.all()

    serializer_class = serializers.ServicioModelSerializer

    def list(self, request, *args, **kwargs):
        """ Listar servicios

            Permite listar todos los servicios registrados en el sistema.
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """ Consultar servicio por ID

            Permite obtener información de un servicio dado su ID
        """
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """ Crear servicios

            Permite crear servicios, .
        """
        serializer = serializers.UpdateAndCreateServicioSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        servicio = serializer.save()
        data = self.get_serializer(instance=servicio).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """ Actualizar servicios
        
            Perimite la actualización de un servicio dado su ID.
        """
        servicio = self.get_object()
        serializer = serializers.UpdateAndCreateServicioSerializer(
            instance=servicio,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        servicio = serializer.save()
        data = self.get_serializer(instance=servicio).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        """Inhabilitar servicio."""
        instance.is_active = False
        instance.save()