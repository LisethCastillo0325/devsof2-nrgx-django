"""Views user."""

# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from django_api.users.models import User

# Serializers
from django_api.users import serializers


class UserViewSet(mixins.ListModelMixin, 
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = serializers.UserModelSerializer

    def get_permissions(self):
        if self.action in ['login']:
            permissions = [AllowAny]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    @action(detail=False, methods=['post'])
    def login(self, request, pk=None):
        serializer = serializers.CustomTokenObtainPairSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': serializers.UserModelSerializer(user).data,
            'token': token
        }
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = serializers.UpdateAndCreateUserSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializers.UserModelSerializer(instance=user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = serializers.UpdateAndCreateUserSerializer(
            instance=user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializers.UserModelSerializer(instance=user).data
        return Response(data=data, status=status.HTTP_201_CREATED)
