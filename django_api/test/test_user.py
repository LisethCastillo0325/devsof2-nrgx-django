import pytest

from django.test import TestCase
from faker import Faker

from django_api.users.models.users import User
from django_api.test.providers.user_providers import EmailProvider


fake = Faker()
fake.add_provider(EmailProvider)

from django_api.users.models.users import User


# @pytest.mark.django_db
# def test_super_user_create(user_creation):
#     print('user:', user_creation.first_name)
#     user_creation.is_superuser = True
#     user_creation.save()
#     assert user_creation.is_superuser

# def test_user_creaction_fail():
#     with pytest.raises(Exception):
#         User.objects.create(
#              email='user@gmail.com'
#         )


class UsuarioTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email=fake.custom_email(), 
            password=fake.phone_number(),
            identification_number='123456789',
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        return super().setUp()
    
    def test_user_creation(self):
        self.assertEqual(self.user.is_superuser, False)