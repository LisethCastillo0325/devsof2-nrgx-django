import pytest

from faker import Faker

from django_api.users.models.users import User
from django_api.test.providers.user_providers import EmailProvider


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
