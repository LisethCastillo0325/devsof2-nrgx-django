"""Users serializers."""

# Django
from django.contrib.auth import authenticate
from django.contrib.auth.signals import user_logged_in

# Django REST Framework
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Models
from django_api.users.models import User

# Utils
from django_api.utils.serializers import DataChoiceSerializer
from django.utils import timezone
from datetime import timedelta


class UserModelSerializer(serializers.ModelSerializer):

    identification_type = DataChoiceSerializer()

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'is_active', 'created', 'updated',
            'email', 'identification_number', 'identification_type', 'birth_date',
            'phone_number', 'is_client', 'groups', 'user_permissions'
        ]


"""
Login serializers
"""

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    """User login serializer"""

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError({'detail': 'Credenciales invalidas.'})
        if not user.is_active:
            raise serializers.ValidationError({'detail': 'Cuenta no activa, por favor comuniquese con el administrador.'})
        self.context['user'] = user
        return super().validate(data)

    def create(self, data):
        """Generate or retrieve new token."""
        token = super().get_token(self.context['user'])
        token['obj_user'] = UserModelSerializer(self.context['user']).data

        user = self.context['user']
        request = self.context['request']
        user_logged_in.send(sender=user.__class__, request=request, user=user)
        token = {
            'refresh': str(token),
            'access': str(token.access_token)
        }
        return self.context['user'], token