import pytest
from faker import Faker

from django_api.users.models.users import User
from django_api.test.providers.user_providers import EmailProvider


fake = Faker()
fake.add_provider(EmailProvider)


@pytest.fixture
def user_creation():
    return User(
        email=fake.custom_email(), 
        password=fake.phone_number(),
        identification_number='123456789',
        first_name=fake.first_name(),
        last_name=fake.last_name()
    )
