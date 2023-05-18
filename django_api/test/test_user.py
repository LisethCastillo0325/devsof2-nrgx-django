import pytest

from faker import Faker

from django_api.users.models.users import User
from django_api.test.providers.user_providers import EmailProvider

from rest_framework.test import APITestCase
from django_api.users.models import User
from rest_framework_simplejwt.tokens import AccessToken
from django.urls import reverse


fake = Faker()
fake.add_provider(EmailProvider)

from django_api.users.models.users import User


@pytest.mark.django_db
def test_super_user_create(user_creation):
    user_creation.is_superuser = True
    user_creation.save()
    assert user_creation.is_superuser

def test_user_creaction_fail():
    with pytest.raises(Exception):
        User.objects.create(
             email='user@gmail.com'
        )


#####

class TestUpdateUserViewSet(APITestCase):
    def setUp(self):
        # Crear un usuario de prueba
        self.user = User.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            identification_number=123456789,
            identification_type=User.IdentificationTypeChoices.CC
        )
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

   # def test_login(self):
        # Realizar una solicitud POST para el inicio de sesión
     #   url = reverse('token_refresh')
    #    data = {
          #  'email': 'test@example.com',
         #   'password': 'password'
        #}
      #  response = self.client.post(url, data)
     # Verificar que la respuesta sea correcta
      #  self.assertEqual(response.status_code, 200)
          # Verificar que el token de acceso esté presente en la respuesta
      #  self.assertIn('access', response.data)


    def test_retrieve_user(self):
        # Realizar una solicitud GET para obtener los detalles del usuario
        url = f'/users/{self.user.id}/'
        response = self.client.get(url)
        # Verificar que la respuesta sea correcta
        self.assertEqual(response.status_code, 200)
        # Verificar los datos devueltos en la respuesta
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User')
        self.assertEqual(response.data['identification_number'], 123456789)



    def test_update_user(self):
        # Realizar una solicitud PATCH para actualizar el usuario
        url = f'/users/{self.user.id}/'

        data = {
            'first_name': 'New First Name',
            'last_name': 'New Last Name'
        }
        response = self.client.patch(url, data=data)
        # Verificar que la respuesta sea correcta
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['first_name'], 'New First Name')
        self.assertEqual(response.data['last_name'], 'New Last Name')


    def test_create_superuser(self):
        """Test creating a superuser."""
        email = "admin@example.com"
        password = "admin123"
        user = User.objects.create_superuser(
            email=email,
            password=password,
            first_name="Admin",
            last_name="User",
            identification_number=123456789,
            identification_type=User.IdentificationTypeChoices.CC
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


    def test_delete_user(self):
    # Realizar una solicitud DELETE para eliminar el usuario
        url = f'/users/{self.user.id}/'
        response = self.client.delete(url)
        # Verificar que la respuesta sea correcta
        self.assertEqual(response.status_code, 204)