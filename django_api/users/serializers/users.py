"""Users serializers."""

# Django
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.signals import user_logged_in

# Django REST Framework
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator

# Models
from django_api.users.models import User
from django.contrib.auth.models import Group

# Utils
from django_api.utils.serializers import DataChoiceSerializer
from django.utils import timezone
from datetime import timedelta
from django_api.utils.custom_regex_validators import CellNumberRegexValidator


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


class UpdateAndCreateUserSerializer(serializers.ModelSerializer):
    """
    Update and create user serializer.
    """
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), 
        lookup='icontains')]
    )
    cel_number_regex = CellNumberRegexValidator(
        message="El formato permitido es 3112224455"
    )
    phone_number = serializers.CharField(validators=[cel_number_regex], max_length=10, required=True)
    identification_number =  serializers.IntegerField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        min_value=111111,
        max_value=9999999999
    )
    identification_type = serializers.ChoiceField(
        choices=User.IdentificationTypeChoices.choices,
        default=User.IdentificationTypeChoices.CC
    )
    birth_date = serializers.DateField(required=False)
    password = serializers.CharField(min_length=6, max_length=30, required=False)
    
    # Relación m2m con la tabla de grupos, conocida tambien como "rol"
    groups = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        many=True
    )

    class Meta:
        """Meta class."""
        model = User
        fields = '__all__'

    def password_validate(self, password):
        password_validation.validate_password(password=password)
        return password

    def create(self, data):
        """
        Crear usuario
        """
        groups_data = data.pop('groups')
        data['password'] = str(data.get('password', data['identification_number']))
        user = User.objects.create(**data)
        user.set_password(data['password'])
        user.save()
        for group in groups_data:
            user.groups.add(group)
        return user

    def update(self, instance, data):
        user = super().update(instance=instance, validated_data=data)
        try:
            user.set_password(data['password'])
            user.password_change_date = timezone.now()
            user.save()
        except KeyError:
            pass
        return user